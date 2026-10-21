import pytest
import yaml
from app.coach import CoachCommand, apply_command
from app.knowledge import DomainError
from app.problem_rules import parse_rules, problem_reply


def start(title="קורקבנים", method="boil_simmer"):
    return apply_command(None, CoachCommand(action="start_custom", dish_title=title, method=method), now=1000)


def change(state, action="answer", **kwargs):
    return apply_command(
        state, CoachCommand(action=action, expected_revision=state["revision"], **kwargs), now=1001
    )


def test_goal_clicks_and_conditional_problem_choices_use_local_rules(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Local choices must not call ordinary dialogue")

    monkeypatch.setattr("app.consultant.contextual_reply", forbidden)
    state = start()
    state = change(state, question_id="condition", answer="thawed_clean")
    assert state["decision_questions"][0]["id"] == "goal"
    state = change(state, question_id="goal", answer="sauce")
    assert state["decision_answers"]["goal"] == "sauce"
    assert "בחרת תבשיל רך ברוטב" in state["messages"][-1]["text"]
    assert state["decision_questions"] == []
    state = change(state, action="problem", problem_id="too_dry")
    assert state["problem_rule_status"] == "clarify"
    assert state["decision_questions"][0]["id"] == "problem_dry_state"
    state = change(state, question_id="problem_dry_state", answer="liquid_low")
    assert state["problem_rule_status"] == "matched"
    assert state["problem_rule_match"]["variant_id"] == "gizzard_liquid_low"
    assert "ציר לא מלוח" in state["messages"][-1]["text"]
    assert not state["pending_problem"] and not state["problem_questions"]
    assert not state["custom_steps"] and state["measured_temperature"] is None


def test_same_problem_has_different_treatments_by_condition_and_dish():
    state = change(start(), action="problem", problem_id="too_dry")
    tough = change(state, question_id="problem_dry_state", answer="hard_wet")
    dry = change(state, question_id="problem_dry_state", answer="cooked_dry")
    assert tough["problem_rule_match"]["variant_id"] == "gizzard_still_tough"
    assert dry["problem_rule_match"]["variant_id"] == "cooked_protein_dry"
    assert tough["messages"][-1]["text"] != dry["messages"][-1]["text"]
    breast = change(start("חזה עוף", "steam"), action="problem", problem_id="too_dry")
    breast = change(breast, question_id="problem_dry_state", answer="hard_wet")
    assert breast["problem_rule_status"] == "missing"
    missing = breast["missing_problem_rules"][-1]
    assert missing["dish_title"] == "חזה עוף" and missing["answers"] == {"dry_state": "hard_wet"}


def test_unknown_condition_is_not_guessed_and_stale_answer_rejected():
    state = change(start(), action="problem", problem_id="too_dry")
    with pytest.raises(DomainError):
        change(state, question_id="problem_dry_state", answer="invented")
    state = change(state, question_id="problem_dry_state", answer="not_sure")
    assert state["problem_rule_status"] == "missing"
    with pytest.raises(DomainError):
        change(state, question_id="problem_dry_state", answer="liquid_low")


def test_tough_gizzards_have_treatment_but_liver_does_not_inherit_it():
    state = change(start(), action="problem", problem_id="tough")
    state = change(state, question_id="problem_tough_state", answer="wet_cooking")
    assert state["problem_rule_match"]["variant_id"] == "gizzard_wet_tough"
    liver = change(start("כבד עוף", "boil_simmer"), action="problem", problem_id="tough")
    liver = change(liver, question_id="problem_tough_state", answer="wet_cooking")
    assert liver["problem_rule_status"] == "missing"


def test_stage_and_method_selectors_and_specific_first_matching_rule():
    state = start()
    state["decision_answers"]["progress"] = "finishing"
    rules = {
        "too_dry": {
            "variants": [
                {"id": "wrong_stage", "response": "This must not match", "stages": ["cooking"]},
                {"id": "wrong_method", "response": "This must not match", "methods": ["steam"]},
                {
                    "id": "correct",
                    "response": "Context matched",
                    "stages": ["finishing"],
                    "methods": ["boil_simmer"],
                },
                {"id": "generic", "response": "Generic response"},
            ]
        }
    }
    assert problem_reply(state, "too_dry", "test", rules) == "Context matched"
    assert state["problem_rule_match"]["variant_id"] == "correct"


@pytest.mark.parametrize(
    "variant",
    [
        {"id": "test", "response": "Valid response", "answers": {"absent": "missing"}},
        {"id": "test", "response": "Valid response", "methods": ["nonexistent"]},
        {"id": "test", "response": "Valid response", "families": ["nonexistent"]},
        {"id": "test", "response": "Valid response", "ingredient_ids": ["nonexistent"]},
    ],
)
def test_invalid_context_rule_references_rejected(variant):
    with pytest.raises(DomainError):
        parse_rules(yaml.safe_dump({"rules": {"too_dry": {"variants": [variant]}}}))


def test_problem_followup_survives_server_restore(env):
    client, headers = env["client"], env["headers"]
    state = client.post(
        "/v1/coach/events",
        headers=headers,
        json={"action": "start_custom", "dish_title": "קורקבנים", "method": "boil_simmer"},
    ).json()
    state = client.post(
        "/v1/coach/events",
        headers=headers,
        json={
            "action": "problem",
            "problem_id": "too_dry",
            "journey_id": state["id"],
            "expected_revision": state["revision"],
        },
    ).json()
    restored = client.get("/v1/coach/current", headers=headers).json()["journey"]
    assert restored["pending_problem"]["problem_id"] == "too_dry"
    result = client.post(
        "/v1/coach/events",
        headers=headers,
        json={
            "action": "answer",
            "question_id": "problem_dry_state",
            "answer": "liquid_low",
            "journey_id": restored["id"],
            "expected_revision": restored["revision"],
        },
    )
    assert result.status_code == 200, result.text
    assert result.json()["problem_rule_match"]["variant_id"] == "gizzard_liquid_low"


def test_default_import_is_preview_only_and_preserves_custom_rules(env):
    draft = {"rules": {"burning": {"response": "תגובה פרטית קיימת שאין להחליף"}}}
    payload = {"yaml_text": yaml.safe_dump(draft, allow_unicode=True)}
    client = env["client"]
    url = "/v1/coach/problem-rules/with-defaults"
    assert client.post(url, json=payload).status_code == 401
    assert client.post(url, headers=env["cook"], json=payload).status_code == 403
    result = client.post(url, headers=env["headers"], json=payload)
    assert result.status_code == 200
    document = yaml.safe_load(result.json()["yaml_text"])
    assert document["rules"]["burning"]["response"] == draft["rules"]["burning"]["response"]
    assert "too_dry" in result.json()["added_ids"] and "tough" in result.json()["added_ids"]
    assert document["rules"]["too_dry"]["questions"]
    assert client.get("/v1/coach/problem-rules", headers=env["headers"]).json()["revision"] == 0
