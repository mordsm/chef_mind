import pytest
from app.coach import CoachCommand, apply_command
from app.knowledge import DomainError


def start(title="קוקבנים"):
    return apply_command(None, CoachCommand(action="start_custom", dish_title=title), now=1000)


def change(state, **kwargs):
    return apply_command(
        state, CoachCommand(action="answer", expected_revision=state["revision"], **kwargs), now=1001
    )


def test_screenshot_answer_is_acknowledged_and_goal_not_repeated():
    state = change(start(), message="תבשיל רך ברוטב")
    assert state["decision_answers"] == {"goal": "sauce"}
    assert "בחרת תבשיל רך ברוטב" in state["messages"][-1]["text"]
    assert "בישול בנוזל" in state["messages"][-1]["text"]
    assert "goal" not in {question["id"] for question in state["decision_questions"]}
    assert not state["custom_steps"]
    assert state["measured_temperature"] is None


def test_click_and_number_follow_same_table_and_persist_method():
    state = start()
    questions = state["decision_questions"]
    numbers = [option["number"] for question in questions for option in question["options"]]
    assert len(numbers) == len(set(numbers))
    method = next(q for q in questions if q["id"] == "method")
    option = next(option for option in method["options"] if option["id"] == "simmer")
    numeric = change(state, message=str(option["number"]))
    clicked = change(state, question_id="method", answer="simmer")
    assert numeric["decision_answers"] == clicked["decision_answers"] == {"method": "simmer"}
    assert numeric["method"] == "בישול בנוזל"
    assert numeric["context"]["method"] == "בישול בנוזל"
    assert numeric["messages"][-1]["text"] == clicked["messages"][-1]["text"]
    state = change(numeric, question_id="condition", answer="thawed_clean")
    state = change(state, question_id="goal", answer="sauce")
    assert state["decision_questions"] == []
    assert "הבחירות נשמרו" in state["messages"][-1]["text"]


def test_invalid_or_stale_choice_does_not_modify_answer():
    state = start()
    invalid = change(state, message="99")
    assert invalid["decision_answers"] == {}
    assert "המספר אינו" in invalid["messages"][-1]["text"]
    with pytest.raises(DomainError, match="Choose an option"):
        change(state, question_id="goal", answer="invented")
    answered = change(state, question_id="goal", answer="sauce")
    with pytest.raises(DomainError):
        change(answered, question_id="goal", answer="brown")


def test_decisions_survive_server_restore_and_new_plan_clears_them(env):
    client, headers = env["client"], env["headers"]
    state = client.post(
        "/v1/coach/events", headers=headers, json={"action": "start_custom", "dish_title": "קוקבנים"}
    ).json()
    result = client.post(
        "/v1/coach/events",
        headers=headers,
        json={
            "action": "answer",
            "journey_id": state["id"],
            "expected_revision": state["revision"],
            "question_id": "goal",
            "answer": "sauce",
        },
    )
    assert result.status_code == 200
    state = client.get("/v1/coach/current", headers=headers).json()["journey"]
    assert state["decision_answers"]["goal"] == "sauce"
    changed = apply_command(
        state,
        CoachCommand(action="update_plan", dish_title="מרק ירקות", expected_revision=state["revision"]),
        now=1002,
    )
    assert changed["decision_answers"] == {}
    assert [q["id"] for q in changed["decision_questions"]] == ["progress"]


def test_unknown_text_never_invents_a_choice():
    state = change(start(), message="אולי משהו אחר")
    assert state["decision_answers"] == {}
    assert len(state["decision_questions"]) == 3
