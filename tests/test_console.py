from conftest import approve, import_doc


def test_console_shell_assets_and_security_headers(env):
    response = env["client"].get("/")
    assert response.status_code == 200
    assert 'dir="rtl"' in response.text
    assert "default-src 'self'" in response.headers["content-security-policy"]
    assert response.headers["cache-control"] == "no-store"
    assert "owner-test-token" not in response.text
    assert env["client"].get("/assets/console.js").status_code == 200
    assert env["client"].get("/assets/console.css").status_code == 200
    assert env["client"].get("/assets/../config.py").status_code == 404
    docs = env["client"].get("/docs")
    assert docs.status_code == 200
    assert "content-security-policy" not in docs.headers  # Swagger uses its own CDN assets.


def test_console_identity_and_private_catalog(env, document):
    assert env["client"].get("/v1/session").status_code == 401
    assert env["client"].get("/v1/knowledge/sources").status_code == 401
    session = env["client"].get("/v1/session", headers=env["headers"]).json()
    assert session == {"user_id": "owner", "role": "reviewer"}
    draft = import_doc(env, document)
    reviewer = env["client"].get("/v1/knowledge/sources", headers=env["headers"]).json()
    assert reviewer["items"][0]["latest_revision_id"] == draft["id"]
    assert reviewer["items"][0]["source_reference"] == document["source_reference"]
    assert reviewer["items"][0]["usage"] == "advanced_advisor_after_approval"
    assert reviewer["items"][0]["tags"] == document["units"][0]["tags"]
    assert env["client"].get("/v1/knowledge/sources", headers=env["cook"]).json()["items"] == []
    assert env["client"].get("/v1/knowledge/sources", headers=env["other"]).json()["items"] == []
    assert approve(env, draft).status_code == 200
    assert (
        env["client"].get("/v1/knowledge/sources", headers=env["cook"]).json()["items"][0]["status"]
        == "active"
    )


def test_cook_catalog_never_shows_new_draft_content(env, document):
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    document["title"] = "Private pending draft title"
    import_doc(env, document, key="private-draft-catalog")
    result = env["client"].get("/v1/knowledge/sources", headers=env["cook"]).json()
    assert result["items"][0]["title"] == "Original onion note"
    assert result["items"][0]["latest_revision_id"] == draft["id"]
    assert "Private pending" not in str(result)


def test_catalog_page_bounds(env):
    for offset in (-1, 100001):
        assert (
            env["client"].get(f"/v1/knowledge/sources?offset={offset}", headers=env["headers"]).status_code
            == 422
        )
    assert env["client"].get("/v1/knowledge/sources?offset=100", headers=env["headers"]).json()["items"] == []
