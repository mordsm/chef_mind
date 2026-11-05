import pytest

from app.coach import CoachCommand, apply_command
from app.gizzard_guidance import report_guidance


def test_gizzards_choices_start_guidance_and_boiling_gets_specific_reply():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="קורקבנים", method="boil_simmer"), 1000)
    for question_id, answer in [("condition", "thawed_clean"), ("goal", "sauce")]:
        state = apply_command(state, CoachCommand(action="answer", question_id=question_id, answer=answer, expected_revision=state["revision"]), 1001)
    assert state["custom_steps"]
    assert not state["decision_questions"]
    assert "דווח כשהנוזל רותח" in state["messages"][-1]["text"]
    assert "90–120" in state["messages"][-1]["text"]
    assert "1 ק״ג" in state["messages"][-1]["text"]
    state = apply_command(state, CoachCommand(action="report", message="הנוזל רתח", expected_revision=state["revision"]), 1002)
    assert "בעבוע עדין" in state["messages"][-1]["text"]
    assert state["completed_step_ids"] == []
    assert state["learning_focus"]["source_ids"] == ["USER_GIZZARD_PROTOCOL_2026_10_25"]


@pytest.mark.parametrize("text", ["הנוזל רתח", "דיווחתי שהנוזל רתח", "המים רותחים", "הנוזל רוטח", "כמה זמן להרתיח?"])
def test_guidance_on_existing_work_without_repeating_choices(text):
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="קורקבנים", method="boil_simmer"), 1000)
    state["decision_answers"] = {"condition": "thawed_clean", "goal": "sauce"}
    state = apply_command(state, CoachCommand(action="report", message=text, expected_revision=state["revision"]), 1001)
    assert state["custom_steps"]
    assert "בעבוע עדין" in state["messages"][-1]["text"]
    assert "90–120" in state["messages"][-1]["text"]
    assert "USER_GIZZARD_PROTOCOL_2026_10_25" in state["learning_focus"]["source_ids"]
    assert not state["completed_step_ids"]


def test_not_boiling_is_not_treated_as_boiling():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="קורקבנים", method="boil_simmer"), 1000)
    assert report_guidance(state, "הנוזל עדיין לא רתח") is None


def test_progress_check_gives_concrete_checks_without_completing_step():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="קורקבנים", method="boil_simmer"), 1000)
    for question_id, answer in [("condition", "thawed_clean"), ("goal", "sauce")]:
        state = apply_command(state, CoachCommand(action="answer", question_id=question_id, answer=answer, expected_revision=state["revision"]), 1001)
    state = apply_command(state, CoachCommand(action="report", message="בדוק את ההתקדמות שלי", expected_revision=state["revision"]), 1002)
    reply = state["messages"][-1]["text"]
    assert "מופשרים ונקיים" in reply
    assert "בעבוע עדין" in reply
    assert not state["completed_step_ids"]


def test_user_protocol_does_not_apply_to_pressure_cooking():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="קורקבנים", method="boil_simmer"), 1000)
    state["context"]["graph"]["method"]["id"] = "pressure"
    assert report_guidance(state, "כמה זמן לבשל?") is None
