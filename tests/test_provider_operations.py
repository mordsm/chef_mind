from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import pytest
from app.config import Settings
from app.model import Selection
from app.provider import ProviderMonitor, error_category
from conftest import approve, chef_body, import_doc


def test_request_budget_and_window_expiry():
    now = [0.0]
    settings = Settings(model_calls_per_minute=3, model_user_calls_per_minute=2)
    monitor = ProviderMonitor(settings, clock=lambda: now[0])
    assert monitor.reserve("owner")
    assert monitor.reserve("owner")
    assert not monitor.reserve("owner")
    assert monitor.reserve("other")
    assert not monitor.reserve("third")
    now[0] = 60.0
    assert monitor.reserve("owner")
    assert monitor.snapshot("owner")["own_calls_last_minute"] == 1


def test_concurrent_budget_reservation():
    monitor = ProviderMonitor(Settings(model_calls_per_minute=3, model_user_calls_per_minute=3))
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: monitor.reserve("owner"), range(20)))
    assert sum(results) == 3


@pytest.mark.parametrize(
    "code,status,expected",
    [
        ("credit_balance_exhausted", 429, "quota_exhausted"),
        ("insufficient_quota", 429, "quota_exhausted"),
        (None, 429, "provider_rate_limited"),
        (None, 401, "authentication_or_access"),
        (None, 403, "authentication_or_access"),
        (None, 500, "provider_error"),
    ],
)
def test_error_categories(code, status, expected):
    assert error_category(SimpleNamespace(code=code, status_code=status)) == expected


def test_rate_limit_fallback_and_owner_isolation(env, document):
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    settings = env["app"].state.settings
    settings.model_enabled = True
    settings.model_user_calls_per_minute = 1
    calls = []

    def selector(*args):
        calls.append(1)
        return Selection(knowledge_id="onion-heat", revision_id=draft["id"])

    env["app"].state.model_selector = selector
    for i in range(2):
        body = chef_body(f"budget-{i}")
        body["allow_external_model"] = True
        response = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body)
        assert response.status_code == 200
        result = response.json()
    assert len(calls) == 1
    assert result["provider_status"] == "local_rate_limited"
    assert result["decision_type"] == "action"
    assert "MODEL_LOCAL_RATE_LIMITED" in result["policy_flags"]
    own = env["client"].get("/v1/operations/provider", headers=env["headers"]).json()
    other = env["client"].get("/v1/operations/provider", headers=env["other"]).json()
    assert own["counts_since_process_start"] == {"selected": 1, "local_rate_limited": 1}
    assert other["counts_since_process_start"] == {}
    assert env["client"].get("/v1/operations/provider", headers=env["cook"]).status_code == 403
    assert "openai_api_key" not in own


def test_stale_state_does_not_spend_model_call(env, document):
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    body = chef_body()
    assert env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).status_code == 200
    env["app"].state.settings.model_enabled = True
    calls = []
    env["app"].state.model_selector = lambda *args: calls.append(1)
    body["allow_external_model"] = True
    assert env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).status_code == 409
    assert not calls


def test_persisted_safety_profile_blocks_before_model(env, document):
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    body = chef_body()
    body["profile"] = {"allergies": ["milk"]}
    assert env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).status_code == 200
    env["app"].state.settings.model_enabled = True
    calls = []
    env["app"].state.model_selector = lambda *args: calls.append(1)
    body.pop("profile")
    body.update(expected_state_revision=1, allow_external_model=True, inventory=[{"name": "milk"}])
    response = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body)
    assert response.status_code == 200
    assert response.json()["decision_type"] == "blocked"
    assert response.json()["provider_status"] == "policy_blocked"
    assert not calls
