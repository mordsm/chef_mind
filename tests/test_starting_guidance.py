from conftest import approve, chef_body, import_doc


def test_missing_knowledge_explains_scope_and_shows_only_approved_topics(env, document):
    body = chef_body()
    body.update(message="unrelatedzzdish", state={"current_goal": "unrelatedzzdish"})
    draft = import_doc(env, document)
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert result["available_topics"] == []
    assert result["decision_type"] == "insufficient_evidence"
    assert approve(env, draft).status_code == 200
    body["cooking_id"] = "new-start"
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert result["available_topics"] == ["onion browning"]
    assert "NO_APPROVED_EVIDENCE" in result["policy_flags"]
    response = env["client"].post("/v1/chef/respond", headers=env["other"], json=body).json()
    assert response["available_topics"] == []


def test_conditions_can_be_confirmed_without_fabricated_reports(env, document):
    document["units"][0]["conditions"] = ["onion is browning before softening"]
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    body = chef_body()
    first = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert first["decision_type"] == "clarify"
    assert first["missing_conditions"] == ["onion is browning before softening"]
    body.update(expected_state_revision=1, confirmed_conditions=first["missing_conditions"])
    response = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert response["decision_type"] == "action"
    assert body["state"].get("reports", []) == []


def test_cut_identification_is_a_short_self_check_with_background(env, document):
    document["source_id"] = "bccampus-meat"
    unit = document["units"][0]
    unit.update(
        knowledge_id="collagen-moist-heat",
        tags=["collagen"],
        conditions=["הנתח זוהה כעשיר ברקמת חיבור ומתאים לבישול לח"],
    )
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    body = chef_body()
    body["message"] = "collagen"
    body["state"]["current_goal"] = "צלי כתף בקר"
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert result["instruction"] == "בדוק שהנתח עשיר ברקמת חיבור."
    assert result["requires_confirmation"] is False
    assert result["proposed_action"] is None  # No cooking/doneness authorization inferred.
    assert len(result["basic_knowledge"]) == 4
    assert all(card["source"].startswith("https://") for card in result["basic_knowledge"])


def test_missing_recipe_still_provides_general_education(env):
    body = chef_body()
    body["message"] = "כנפי הודו בתנור"
    result = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body).json()
    assert result["decision_type"] == "insufficient_evidence"
    assert result["basic_knowledge"]
    assert result["citations"] == []  # Educational sources are separate from action grounding.
