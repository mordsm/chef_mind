from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from app.db import ActionLogEntry, ActionLogMutation, session_factory
from sqlalchemy import func, select


def mutation(client, headers, cooking_id, kind="create_session", **fields):
    body = {"request_id": str(uuid4()), "kind": kind, "cooking_id": cooking_id, **fields}
    return body, client.post("/v1/action-log/mutations", headers=headers, json=body)


def setup_session(env):
    cooking_id = str(uuid4())
    _, response = mutation(env["client"], env["headers"], cooking_id)
    assert response.status_code == 200, response.text
    return cooking_id


def report(action="cut", minutes_ago=0):
    parameters = {"ingredient": "onion", "cut_type": "cubes", "size": "medium"}
    if action == "cook":
        parameters = {"temperature": None, "duration": 30, "equipment": "pot"}
    return {
        "action_type": action,
        "config_version": 1,
        "parameters": parameters,
        "started_at": (datetime.now(UTC) - timedelta(minutes=minutes_ago)).isoformat(),
        "notes": "",
    }


def test_report_pages_manifest_and_scope_are_available(env):
    client = env["client"]
    assert client.get("/report/").status_code == 200
    assert client.get("/report/").headers["Content-Security-Policy"]
    assert client.get("/report/sw.js").status_code == 200
    manifest = client.get("/assets/report/manifest.webmanifest").json()
    assert manifest["scope"] == "/report/"
    for icon in manifest["icons"]:
        assert client.get(icon["src"]).content.startswith(b"\x89PNG")
    assert len(client.get("/v1/action-log/config").json()["actions"]) == 13
    assert client.get("/v1/action-log/sessions").status_code == 401


def test_owner_scoped_sessions_reports_and_linked_coach(env):
    client, headers = env["client"], env["headers"]
    cooking_id = setup_session(env)
    assert client.get("/v1/action-log/sessions", headers=env["other"]).json()["items"] == []
    assert client.get(f"/v1/action-log/sessions/{cooking_id}", headers=env["other"]).status_code == 404
    _, denied = mutation(client, headers, str(uuid4()), linked_cooking_id="another-persons-coach")
    assert denied.status_code == 404
    state = client.post("/v1/coach/events", headers=headers, json={"action": "start"}).json()
    _, linked = mutation(
        client, headers, str(uuid4()), linked_cooking_id=state["id"], recipe_id=state["recipe_id"]
    )
    assert linked.status_code == 200


def test_lost_response_retry_is_exact_and_does_not_repeat_effect(env):
    client, headers = env["client"], env["headers"]
    cooking_id = setup_session(env)
    body, response = mutation(client, headers, cooking_id, "put", report_id=str(uuid4()), report=report())
    assert response.status_code == 200, response.text
    assert client.post("/v1/action-log/mutations", headers=headers, json=body).json() == response.json()
    body["report"]["notes"] = "different"
    assert client.post("/v1/action-log/mutations", headers=headers, json=body).status_code == 409
    with session_factory(env["engine"])() as db:
        assert db.scalar(select(func.count()).select_from(ActionLogEntry)) == 1
        assert db.scalar(select(func.count()).select_from(ActionLogMutation)) == 2


def test_edit_conflict_retains_current_version_and_deletion_is_a_tombstone(env):
    client, headers = env["client"], env["headers"]
    cooking_id = setup_session(env)
    report_id = str(uuid4())
    _, first = mutation(client, headers, cooking_id, "put", report_id=report_id, report=report())
    assert first.status_code == 200
    updated = report()
    updated["parameters"]["size"] = "fine"
    _, edited = mutation(
        client, headers, cooking_id, "put", report_id=report_id, report=updated, expected_revision=1
    )
    assert edited.json()["report"]["revision"] == 2
    _, stale = mutation(
        client, headers, cooking_id, "put", report_id=report_id, report=report(), expected_revision=1
    )
    assert stale.status_code == 409
    assert stale.json()["current"]["parameters"]["size"] == "fine"
    _, deleted = mutation(client, headers, cooking_id, "delete", report_id=report_id, expected_revision=2)
    assert deleted.json()["report"]["deleted"]
    _, resurrection = mutation(
        client, headers, cooking_id, "put", report_id=report_id, report=report(), expected_revision=3
    )
    assert resurrection.status_code == 409
    snapshot = client.get(f"/v1/action-log/sessions/{cooking_id}", headers=headers).json()
    assert snapshot["session"]["revision"] == 3
    assert snapshot["reports"][0]["deleted"]


@pytest.mark.parametrize(
    "change",
    [
        lambda r: r["parameters"].update(size="anything I typed"),
        lambda r: r["parameters"].update(extra="field"),
        lambda r: r.update(action_type="unconfigured"),
        lambda r: r.update(config_version=999),
        lambda r: r["parameters"].update(ingredient="not-in-list"),
    ],
)
def test_only_configured_parameters_are_accepted(env, change):
    cooking_id = setup_session(env)
    value = report()
    change(value)
    _, response = mutation(
        env["client"], env["headers"], cooking_id, "put", report_id=str(uuid4()), report=value
    )
    assert response.status_code == 422


def test_timer_uses_reported_start_and_preserves_unknown_temperature(env):
    cooking_id = setup_session(env)
    _, response = mutation(
        env["client"], env["headers"], cooking_id, "put", report_id=str(uuid4()), report=report("cook", 31)
    )
    row = response.json()["report"]
    assert row["parameters"]["temperature"] is None
    assert datetime.fromisoformat(row["scheduled_end_at"]) - datetime.fromisoformat(
        row["started_at"]
    ) == timedelta(minutes=30)
    assert row["timer_elapsed_at"] == row["scheduled_end_at"]
    assert row["ended_at"] is None


def test_boolean_is_not_a_numeric_parameter(env):
    cooking_id = setup_session(env)
    value = report("cook")
    value["parameters"]["duration"] = True
    _, response = mutation(
        env["client"], env["headers"], cooking_id, "put", report_id=str(uuid4()), report=value
    )
    assert response.status_code == 422


def test_another_device_gets_changes_by_long_poll(env):
    cooking_id = setup_session(env)
    client, headers = env["client"], env["headers"]
    with ThreadPoolExecutor(max_workers=1) as pool:
        waiting = pool.submit(
            client.get, f"/v1/action-log/sessions/{cooking_id}?after=0&wait=5", headers=headers
        )
        _, response = mutation(client, headers, cooking_id, "put", report_id=str(uuid4()), report=report())
        assert response.status_code == 200
        snapshot = waiting.result(timeout=7).json()
    assert snapshot["reports"][0]["action_type"] == "cut"
    assert snapshot["session"]["revision"] == 1
