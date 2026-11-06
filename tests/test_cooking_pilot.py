import pytest
from app.coach import CoachCommand, JourneyState, apply_command
from app.cooking_pilot import timer_request


def change(state, action, now=20, **kwargs):
    return apply_command(
        JourneyState.model_validate(state).model_dump(),
        CoachCommand(action=action, expected_revision=state["revision"], **kwargs),
        now,
    )


def salad():
    state = apply_command(
        None,
        CoachCommand(
            action="start_custom",
            dish_title="סלט ירקות עם רוטב לימון ושמן",
            ingredients=["מלפפון", "עגבנייה", "חסה", "שמן זית", "לימון", "מלח"],
        ),
        1,
    )
    return change(
        state,
        "intake",
        intake_facts={"family": "vegetables", "quantity": "500 גרם", "equipment": "other", "goal": "crisp"},
    )


def test_pilot_leads_without_manual_step_creation_and_requires_explicit_completion():
    state = salad()
    assert len(state["custom_steps"]) == 4
    assert "500 גרם" in state["station_protocol"]["current_action"]["text"]
    assert "סבון" in state["station_protocol"]["current_action"]["text"]
    assert "ללא חימום" in state["station_protocol"]["blocks"][1]["text"]
    original = state["original_dish_title"]
    state = change(state, "ask", message="הרוטב חמוץ מדי והסלט מוציא מים")
    assert "כף מהרוטב" in state["station_protocol"]["current_action"]["text"]
    assert not state["completed_step_ids"]
    state = change(state, "ask", message="אין לי לימון. יש חומץ. איך להחליף בלי שהרוטב יהיה חמוץ מדי?")
    assert "טיפות חומץ" in state["station_protocol"]["current_action"]["text"]
    assert state["cooking_memory"]["reported_problem"] == "הרוטב חמוץ מדי והסלט מוציא מים"
    state = change(state, "ask", message="מה פירוש שליקה? זו שאלה צדדית")
    assert state["original_dish_title"] == original
    state = change(state, "ask", message="חזור לבישול: מה התקלה ומה חסר לי?")
    text = state["station_protocol"]["current_action"]["text"]
    assert "חמוץ מדי" in text and "אין לי לימון" in text
    assert not state["completed_step_ids"]
    for _ in range(4):
        state = change(state, "complete")
    assert len(state["completed_step_ids"]) == 4
    state = change(state, "ask", message="איך להגיש ולשמור מה שנשאר?")
    assert "מתחת ל־4°C" in state["station_protocol"]["current_action"]["text"]
    state = change(state, "finish")
    assert state["status"] == "completed" and state["completion_summary"]


def test_explicit_timer_request_sets_real_deadline_and_expiry_question():
    state = salad()
    state = change(state, "ask", now=100, message="הפעל תזכורת אמיתית לבדוק בעוד שתי שניות")
    assert state["timer_deadline"] == 102
    assert "תזכורת" in state["station_protocol"]["current_action"]["text"]
    state = change(state, "check_in", now=103)
    assert "time" in state["asked"]
    assert "מה מצב המנה" in state["station_protocol"]["current_action"]["text"]


@pytest.mark.parametrize(
    "message",
    [
        "אל תפעיל תזכורת ל־2 דקות",
        "למה צריך טיימר של 2 דקות?",
        "set timer for 999999 minutes",
        "set timer for 1.5 minutes",
        "set timer for -2 minutes",
    ],
)
def test_non_requests_and_unbounded_times_do_not_start_timer(message):
    assert timer_request(message) is None


def test_unknown_or_unsafe_composition_does_not_enter_cold_vegetable_pilot():
    state = apply_command(
        None,
        CoachCommand(action="start_custom", dish_title="סלט ירקות", ingredients=["עגבניות ועוף", "מלפפון"]),
        1,
    )
    state = change(state, "intake", intake_facts={"family": "vegetables", "quantity": "500 גרם"})
    assert not state["custom_steps"]
