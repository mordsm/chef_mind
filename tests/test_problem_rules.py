import yaml
from app.coach import CoachCommand, apply_command


def start():
    return apply_command(None, CoachCommand(action="start_custom", dish_title="קוקבנים"), now=1000)


def report(state, **kwargs):
    return apply_command(
        state, CoachCommand(action="problem", expected_revision=state["revision"], **kwargs), now=1001
    )


def test_chooser_and_supported_problem_return_specific_rule():
    state = report(start())
    assert state["problem_rule_status"] == "choose"
    assert any(option["id"] == "too_thick" for option in state["problem_options"])
    state = report(state, problem_id="too_thick")
    assert state["problem_rule_status"] == "matched"
    assert "מעט נוזל" in state["messages"][-1]["text"]
    assert state["missing_problem_rules"] == []


def test_missing_rule_records_description_without_inventing_response():
    state = report(start(), problem_id="other", message="בעיה שאינה מוגדרת")
    assert state["problem_rule_status"] == "missing"
    assert "חסר חוק" in state["messages"][-1]["text"]
    missing = state["missing_problem_rules"][0]
    assert missing["problem_id"] == "other" and missing["description"] == "בעיה שאינה מוגדרת"
    assert missing["dish_title"] == "קוקבנים" and missing["method"] == ""
    assert not state["custom_steps"]


def test_exact_free_text_problem_uses_same_rule_and_fire_always_pauses():
    state = apply_command(
        start(), CoachCommand(action="report", message="מלוח מדי", expected_revision=1), now=1001
    )
    assert state["problem_rule_status"] == "matched"
    assert "אל תוסיף עוד מלח" in state["messages"][-1]["text"]
    state = report(state, problem_id="fire")
    assert state["safety_hold"] and state["status"] == "paused"
    assert state["problem_rule_status"] == "safety"


def test_private_rule_edit_requires_review_and_is_scoped_and_live(env):
    client, headers = env["client"], env["headers"]
    base = client.get("/v1/coach/problem-rules/template").json()
    assert client.get("/v1/coach/problem-rules").status_code == 401
    document = yaml.safe_load(base["yaml_text"])
    document["rules"]["too_dry"] = {
        "response": "נוספה תגובה בדוקה: דווח אילו מרכיבים כבר הוספת לפני שינוי במנה."
    }
    text = yaml.safe_dump(document, allow_unicode=True)
    body = {"expected_revision": 0, "yaml_text": text, "reviewed": False}
    assert client.put("/v1/coach/problem-rules", headers=headers, json=body).status_code == 422
    body["reviewed"] = True
    assert client.put("/v1/coach/problem-rules", headers=env["cook"], json=body).status_code == 403
    assert client.put("/v1/coach/problem-rules", headers=headers, json=body).status_code == 200
    assert client.put("/v1/coach/problem-rules", headers=headers, json=body).status_code == 409
    assert client.get("/v1/coach/problem-rules", headers=env["other"]).json()["revision"] == 0
    assert "too_dry" in client.get("/v1/coach/problem-rules/template").json()["rules"]
    state = client.post(
        "/v1/coach/events", headers=headers, json={"action": "start_custom", "dish_title": "קוקבנים"}
    ).json()
    response = client.post(
        "/v1/coach/events",
        headers=headers,
        json={
            "action": "problem",
            "problem_id": "too_dry",
            "journey_id": state["id"],
            "expected_revision": state["revision"],
        },
    )
    assert response.status_code == 200
    assert response.json()["problem_rule_status"] == "matched"
    assert "נוספה תגובה בדוקה" in response.json()["messages"][-1]["text"]
    guest = report(start(), problem_id="too_dry")
    assert guest["problem_rule_status"] == "clarify"


def test_method_specific_rule_and_non_overridable_fire(env):
    client, headers = env["client"], env["headers"]
    for text in [
        "rules: {fire: {response: 'Do not pause the cooking'}}",
        "rules: {unknown: {response: 'Unknown rule'}}",
        "rules: {too_dry: {response: 1}}",
    ]:
        response = client.put(
            "/v1/coach/problem-rules",
            headers=headers,
            json={
                "expected_revision": 0,
                "yaml_text": text,
                "reviewed": True,
            },
        )
        assert response.status_code == 422
    custom = {"too_dry": {"response": "תגובה בדוקה למחבת בלבד", "methods": ["מחבת"]}}
    state = apply_command(
        start(),
        CoachCommand(action="problem", problem_id="too_dry", expected_revision=1),
        now=1001,
        problem_rules=custom,
    )
    assert state["problem_rule_status"] == "missing"
