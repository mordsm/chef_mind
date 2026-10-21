import copy

from app.db import AuditEvent, IndexedUnit
from conftest import approve, chef_body, import_doc, write_document
from sqlalchemy import select
from sqlalchemy.orm import Session


def ask(env, body=None, headers=None):
    return env["client"].post("/v1/chef/respond", headers=headers or env["headers"], json=body or chef_body())


def test_import_approve_answer_and_citation_are_end_to_end(env, document):
    draft = import_doc(env, document)
    response = ask(env)
    assert response.status_code == 200
    assert response.json()["decision_type"] == "insufficient_evidence"
    activated = approve(env, draft)
    assert activated.status_code == 200, activated.text
    assert activated.json()["status"] == "active"
    result = ask(env, chef_body("dinner-2")).json()
    assert result["decision_type"] == "action"
    assert result["instruction"] == document["units"][0]["recommended_action"]
    assert result["culinary_reason"] and result["success_signal"]
    assert result["estimated_check_time"] is None
    assert result["citations"][0]["revision_id"] == draft["id"]
    assert result["citations"][0]["supporting_text"] == result["instruction"]
    assert result["constitution_version"] == "0.1"
    assert len(result["constitution_digest"]) == 64
    assert "לפי הדיווח שלך" in result["response_text"]


def test_idempotency_hash_dedup_and_changed_key_conflict(env, document):
    first = import_doc(env, document)
    assert import_doc(env, document)["id"] == first["id"]
    assert import_doc(env, document, "other-test-key")["id"] == first["id"]
    document["title"] = "Changed content"
    write_document(env, document)
    conflict = env["client"].post(
        "/v1/knowledge/import",
        headers=env["headers"],
        json={"path": "note.md", "idempotency_key": "import-test-001"},
    )
    assert conflict.status_code == 409
    assert conflict.json()["code"] == "IDEMPOTENCY_CONFLICT"


def test_revision_update_deletion_and_failed_gate_preserve_old_active(env, document):
    first = import_doc(env, document)
    assert approve(env, first).status_code == 200
    document["units"][0]["recommended_action"] = "Reduce heat and inspect the onion."
    second = import_doc(env, document, "second-revision-key")
    assert second["revision"] == 2
    assert ask(env).json()["citations"][0]["revision_id"] == first["id"]
    (env["root"] / "owner" / "note.md").unlink()
    env["app"].state.activation_gate = lambda doc: {"passed": False, "cases": []}
    failed = approve(env, second)
    assert failed.status_code == 409
    assert ask(env, chef_body("another-run")).json()["citations"][0]["revision_id"] == first["id"]
    with Session(env["engine"]) as session:
        assert session.scalar(select(AuditEvent).where(AuditEvent.action == "ACTIVATION_GATE_FAILED"))


def test_embedding_failure_does_not_activate_partial_revision(env, document):
    draft = import_doc(env, document)

    def fail(text):
        raise RuntimeError("internal private provider details")

    env["app"].state.embed = fail
    # TestClient normally re-raises server failures; use a non-raising client for the sanitized envelope.
    from fastapi.testclient import TestClient

    with TestClient(env["app"], raise_server_exceptions=False) as client:
        result = client.post(
            f"/v1/knowledge/{draft['id']}/approve",
            headers=env["headers"],
            json={"expected_revision": 1, "reason": "Reviewed original source"},
        )
        assert result.status_code == 500
        assert "private provider" not in result.text
    assert ask(env).json()["decision_type"] == "insufficient_evidence"
    with Session(env["engine"]) as session:
        assert not session.scalars(select(IndexedUnit)).all()


def test_license_conflicts_rejection_and_stale_review(env, document):
    document["license_status"] = "unknown"
    first = import_doc(env, document)
    assert approve(env, first).json()["code"] == "LICENSE_UNVERIFIED"
    document["license_status"] = "original"
    document["units"][0]["conflicts_with"] = ["competing-principle"]
    second = import_doc(env, document, "second-import-key")
    assert approve(env, first).status_code == 409
    assert approve(env, second).json()["code"] == "UNRESOLVED_CONFLICT"
    rejected = env["client"].post(
        f"/v1/knowledge/{second['id']}/reject",
        headers=env["headers"],
        json={"expected_revision": 2, "reason": "Contradiction needs review"},
    )
    assert rejected.json()["status"] == "rejected"
    assert ask(env).json()["citations"] == []


def test_successful_new_revision_replaces_index_without_restart(env, document):
    first = import_doc(env, document)
    assert approve(env, first).status_code == 200
    document["units"][0]["recommended_action"] = "Monitor onion while reducing heat."
    second = import_doc(env, document, "new-version-test-key")
    assert approve(env, second).status_code == 200
    result = ask(env).json()
    assert result["citations"][0]["revision_id"] == second["id"]
    assert result["instruction"] == document["units"][0]["recommended_action"]


def test_two_supported_techniques_have_two_traceable_citations(env, document):
    second = copy.deepcopy(document["units"][0])
    second["knowledge_id"] = "onion-other-technique"
    second["recommended_action"] = "Take the onion pan off heat briefly while monitoring."
    document["units"].append(second)
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    body = chef_body()
    body["compare_techniques"] = True
    result = ask(env, body).json()
    assert result["decision_type"] == "action" and len(result["alternatives"]) == 1
    assert len(result["citations"]) == 2
    assert {c["supporting_text"] for c in result["citations"]} == {
        result["instruction"],
        result["alternatives"][0],
    }
