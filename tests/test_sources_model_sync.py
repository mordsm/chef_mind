from pathlib import Path

import pytest
from app.culinary_evaluation import run_culinary_suite
from app.db import session_factory
from app.knowledge import read_document
from app.model import Selection
from conftest import approve, chef_body, import_doc, write_document


def install_corpus(env):
    corpus = Path(__file__).resolve().parents[1] / "vault" / "owner" / "00_inbox"
    for path in corpus.glob("*.md"):
        if path.name == "onion-demo.md":
            continue
        (env["root"] / "owner" / path.name).write_bytes(path.read_bytes())
    response = env["client"].post("/v1/vault/sync", headers=env["headers"])
    assert response.status_code == 200, response.text
    assert not response.json()["errors"]
    for item in response.json()["items"]:
        draft = env["client"].get(f"/v1/knowledge/{item['revision_id']}", headers=env["headers"]).json()
        assert approve(env, draft).status_code == 200


def test_licensed_corpus_cooking_scenarios(env):
    install_corpus(env)
    with session_factory(env["engine"])() as session:
        report = run_culinary_suite(session, "owner")
    assert len(report["cases"]) == 20
    assert report["passed"], report


def test_sync_changes_never_activate_or_delete(env, document):
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    document["units"][0]["recommended_action"] = "Turn down heat and watch the onion carefully."
    target = write_document(env, document)
    synced = env["client"].post("/v1/vault/sync", headers=env["headers"]).json()
    assert synced["items"][0]["status"] == "pending_review"
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=chef_body()).json()
    assert result["citations"][0]["revision_id"] == draft["id"]
    target.unlink()
    synced = env["client"].post("/v1/vault/sync", headers=env["headers"]).json()
    assert synced["missing_sources"] == [document["source_id"]]


def test_sync_duplicates_invalid_files_and_roles(env, document):
    write_document(env, document)
    write_document(env, document, path="duplicate.md")
    (env["root"] / "owner" / "broken.md").write_text("---\nnot: [valid\n---", encoding="utf-8")
    response = env["client"].post("/v1/vault/sync", headers=env["headers"]).json()
    assert len(response["errors"]) == 3
    assert not response["items"]
    assert env["client"].post("/v1/vault/sync", headers=env["cook"]).status_code == 403


def test_model_opt_in_and_fallback(env, document):
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    calls = []

    def selector(settings, body, candidates):
        calls.append(body.message)
        return Selection(knowledge_id="onion-heat", revision_id=draft["id"])

    env["app"].state.model_selector = selector
    # Settings are captured by the app, so make the model toggle accessible in tests/configuration.
    env["app"].state.settings.model_enabled = True
    body = chef_body()
    response = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body)
    assert response.status_code == 200
    assert calls == []
    body.update(cooking_id="model-dinner", allow_external_model=True)
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert calls and result["engine_version"] == "openai-approved-selector-v1"
    assert result["instruction"] == document["units"][0]["recommended_action"]

    def unavailable(*args):
        raise TimeoutError("private provider details must never leak")

    env["app"].state.model_selector = unavailable
    body["cooking_id"] = "fallback"
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert "MODEL_UNAVAILABLE_EXTRACTIVE_FALLBACK" in result["policy_flags"]
    assert "private provider" not in str(result)


def test_model_rejects_unapproved_selection(env, document):
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    env["app"].state.settings.model_enabled = True
    env["app"].state.model_selector = lambda *args: Selection(knowledge_id="fake", revision_id="fake")
    body = chef_body()
    body["allow_external_model"] = True
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert result["decision_type"] == "insufficient_evidence"
    assert result["policy_flags"] == ["MODEL_SOURCE_STALE"]


@pytest.mark.parametrize(
    "filename",
    [
        "bccampus-starch.md",
        "bccampus-custard.md",
        "bccampus-sugar.md",
        "bccampus-meat.md",
        "usda-thermometer.md",
    ],
)
def test_corpus_has_attribution(filename):
    root = Path(__file__).resolve().parents[1] / "vault"
    document, _, _ = read_document(root, "owner", "00_inbox/" + filename)
    assert document.attribution and document.adaptation_notes
    assert document.license_status != "unknown"
