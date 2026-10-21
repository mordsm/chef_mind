from conftest import approve, chef_body, import_doc


def post(env, revision, operation, active):
    return env["client"].post(
        f"/v1/knowledge/{revision['id']}/{operation}",
        headers=env["headers"],
        json={"expected_active_revision_id": active, "reason": "Explicit reviewer lifecycle decision"},
    )


def test_history_diff_rollback_and_retirement(env, document):
    first = import_doc(env, document)
    assert approve(env, first).status_code == 200
    document["units"][0]["recommended_action"] = "Reduce heat and observe onion browning closely."
    second = import_doc(env, document, key="second-revision-key")
    assert approve(env, second).status_code == 200
    path = f"/v1/knowledge/{second['id']}"
    history = env["client"].get(path + "/revisions", headers=env["headers"]).json()
    assert [r["revision"] for r in history["items"]] == [2, 1]
    assert history["active_revision_id"] == second["id"]
    diff = env["client"].get(path + f"/diff/{first['id']}", headers=env["headers"]).json()
    assert "+" in diff["diff"] and "Reduce heat" in diff["diff"]
    assert post(env, first, "rollback", first["id"]).status_code == 409
    assert post(env, first, "rollback", second["id"]).status_code == 200
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=chef_body()).json()
    assert result["citations"][0]["revision_id"] == first["id"]
    assert post(env, first, "retire", first["id"]).status_code == 200
    body = chef_body("after-retire")
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert result["decision_type"] == "insufficient_evidence"
    assert post(env, first, "rollback", None).status_code == 200


def test_lifecycle_permissions_and_pending_rollback(env, document):
    draft = import_doc(env, document)
    assert post(env, draft, "rollback", None).status_code == 409
    for suffix in ("revisions", f"diff/{draft['id']}"):
        path = f"/v1/knowledge/{draft['id']}/{suffix}"
        assert env["client"].get(path, headers=env["other"]).status_code == 404
        assert env["client"].get(path, headers=env["cook"]).status_code == 403
    for operation in ("retire", "rollback"):
        path = f"/v1/knowledge/{draft['id']}/{operation}"
        body = {"expected_active_revision_id": None, "reason": "Review attempt"}
        assert env["client"].post(path, headers=env["other"], json=body).status_code == 404
        assert env["client"].post(path, headers=env["cook"], json=body).status_code == 403


def test_rollback_gate_failure_preserves_current(env, document):
    first = import_doc(env, document)
    assert approve(env, first).status_code == 200
    document["units"][0]["principle"] = "Less heat changes browning speed."
    second = import_doc(env, document, key="second-gate-revision")
    assert approve(env, second).status_code == 200
    env["app"].state.activation_gate = lambda doc: {"passed": False, "reason": "regression"}
    assert post(env, first, "rollback", second["id"]).status_code == 409
    history = env["client"].get(f"/v1/knowledge/{first['id']}/revisions", headers=env["headers"]).json()
    assert history["active_revision_id"] == second["id"]


def test_diff_rejects_different_sources(env, document):
    first = import_doc(env, document)
    document["source_id"] = "another-source"
    second = import_doc(env, document, key="other-source-key")
    response = env["client"].get(f"/v1/knowledge/{first['id']}/diff/{second['id']}", headers=env["headers"])
    assert response.status_code == 409
