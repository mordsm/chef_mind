import pytest
from app.coach import CoachCommand, JourneyState, apply_command
from app.dish_plans import active_plan

CASES = {
    "beef": (
        "תבשיל בקר בבישול ארוך",
        ["שוק בקר", "בצל", "גזר", "שמן זית", "מלח", "מים"],
        "meat",
        "pot",
        "boil_simmer",
    ),
    "fish": ("פילה סלמון בתנור", ["סלמון", "לימון", "שמן זית", "מלח"], "fish", "oven", "oven_roast"),
    "legumes": (
        "תבשיל עדשים וירקות",
        ["עדשים ירוקות יבשות", "גזר", "בצל", "עגבניות", "מים", "מלח"],
        "legumes",
        "pot",
        "boil_simmer",
    ),
    "soup": (
        "מרק ירקות עשיר",
        ["גזר", "קישוא", "תפוח אדמה", "בצל", "שמן זית", "מים", "מלח"],
        "soup",
        "pot",
        "boil_simmer",
    ),
    "bread": ("לחם שמרים פשוט", ["קמח חיטה", "שמרים יבשים", "מים", "מלח", "שמן"], "starch", "oven", ""),
}


def change(state, action, **extra):
    return apply_command(
        JourneyState.model_validate(state).model_dump(),
        CoachCommand(action=action, expected_revision=state["revision"], **extra),
        100,
    )


def begin(key, **overrides):
    title, ingredients, family, equipment, method = CASES[key]
    state = apply_command(
        None, CoachCommand(action="start_custom", dish_title=title, ingredients=ingredients), 1
    )
    facts = {
        "family": family,
        "equipment": equipment,
        "method": method,
        "quantity": "500 גרם",
        "cut": "פילה בעובי 3 ס״מ" if key == "fish" else "קוביות 3 ס״מ",
        "goal": "soft",
        **overrides,
    }
    return change(state, "intake", intake_facts=facts)


@pytest.mark.parametrize("key", CASES)
def test_full_plan_roundtrips_and_leads_to_serving_without_manual_steps(key):
    state = begin(key)
    assert active_plan(state)[0] == key
    assert len(state["custom_steps"]) >= 4
    assert not state["intake_guidance"]["recipe_requested"]
    assert "UNKNOWN" not in state["station_protocol"]["blocks"][1]["text"]
    assert any(ref.get("revision_sha256") for ref in state["station_protocol"]["editorial_references"])
    original = state["original_dish_title"]
    state = change(state, "ask", message="מה פירוש שליקה? זו שאלה צדדית")
    assert state["original_dish_title"] == original and not state["completed_step_ids"]
    for _ in range(len(state["custom_steps"])):
        current = state["custom_steps"][state["current_step"]]
        if current["minimum_temperature"] is not None:
            before = len(state["completed_step_ids"])
            state = change(state, "complete")
            assert len(state["completed_step_ids"]) == before
            assert "אל תעבור" in state["station_protocol"]["current_action"]["text"]
            state = change(state, "report", temperature=current["minimum_temperature"] - 1)
            state = change(state, "complete")
            assert len(state["completed_step_ids"]) == before
            state = change(state, "report", temperature=current["minimum_temperature"])
        state = change(state, "complete")
    assert len(state["completed_step_ids"]) == len(state["custom_steps"])
    state = change(state, "ask", message="איך להגיש ולשמור מה שנשאר?")
    assert (
        "הגש" in state["station_protocol"]["current_action"]["text"]
        or "צנן" in state["station_protocol"]["current_action"]["text"]
    )
    state = change(state, "finish")
    assert state["status"] == "completed"
    assert not any("מנוחה" in line for line in state["completion_summary"])


@pytest.mark.parametrize(
    "key,problem,missing,expected",
    [
        ("beef", "הבשר עדיין קשה", "אין לי ציר בקר. יש רק מים", "כיסוי הבשר"),
        ("fish", "הסלמון יבש ומתפרק", "אין לי לימון. יש חומץ", "טיפה"),
        ("legumes", "העדשים עדיין קשות", "אין לי עגבניות", "לוותר"),
        ("soup", "המרק דליל ומימי", "אין לי בצל. יש כרישה", "בין השכבות"),
        ("bread", "הבצק לא תפח", "אין לי שמרים יבשים. יש טריים", "האריזה"),
    ],
)
def test_failure_missing_ingredient_and_return_preserve_operational_memory(key, problem, missing, expected):
    state = begin(key)
    state = change(state, "ask", message=problem)
    assert state["cooking_memory"]["reported_problem"] == problem
    state = change(state, "ask", message=missing)
    assert expected in state["station_protocol"]["current_action"]["text"]
    state = change(state, "ask", message="מה פירוש שליקה?")
    state = change(state, "ask", message="חזור לבישול: מה התקלה ומה חסר לי?")
    assert problem in state["station_protocol"]["current_action"]["text"]
    assert missing in state["station_protocol"]["current_action"]["text"]


def test_changed_intake_invalidates_generated_steps_measurements_and_timer():
    state = begin("beef")
    prior = {step["id"] for step in state["custom_steps"]}
    state = change(state, "timer", seconds=60)
    state = change(state, "intake", intake_facts={**state["intake_facts"], "quantity": "1 ק״ג"})
    assert prior.isdisjoint(step["id"] for step in state["custom_steps"])
    assert state["timer_deadline"] is None
    assert "1 ק״ג" in state["station_protocol"]["current_action"]["text"]


def test_skipping_to_serving_does_not_bypass_cooking_confirmation():
    state = begin("fish")
    state = change(state, "select_step", step_id=state["custom_steps"][-1]["id"])
    state = change(state, "complete")
    assert not state["completed_step_ids"]
    assert "טרם אישרת" in state["station_protocol"]["current_action"]["text"]


def test_measurement_from_another_step_cannot_unlock_cooking():
    state = begin("fish")
    state = change(state, "report", temperature=70)
    cook = next(s for s in state["custom_steps"] if s["minimum_temperature"] is not None)
    cook["minimum_temperature"] = None
    state = change(state, "select_step", step_id=cook["id"])
    state = change(state, "complete")
    assert not state["completed_step_ids"]
    assert state["measured_temperature"] is None


def test_removed_cooking_check_does_not_crash_or_unlock_serving():
    state = begin("fish")
    cook = next(s for s in state["custom_steps"] if s["minimum_temperature"] is not None)
    state = change(state, "remove_step", step_id=cook["id"])
    state = change(state, "select_step", step_id=state["custom_steps"][-1]["id"])
    state = change(state, "complete")
    assert not state["completed_step_ids"]
    assert "הוסר" in state["station_protocol"]["current_action"]["text"]


@pytest.mark.parametrize("key", CASES)
def test_wrong_equipment_does_not_silently_change_recipe_method(key):
    state = begin(key, equipment="grill")
    assert not active_plan(state)[1]


def test_unknown_extra_ingredient_or_wrong_lentil_type_is_not_ignored():
    state = begin("legumes")
    state = change(
        state,
        "update_plan",
        dish_title=state["dish_title"],
        ingredients=["שעועית אדומה יבשה", "גזר", "בצל", "מים"],
    )
    state = change(
        state,
        "intake",
        intake_facts={
            "family": "legumes",
            "equipment": "pot",
            "quantity": "500 גרם",
            "method": "boil_simmer",
        },
    )
    assert not active_plan(state)[1]
    assert state["station_protocol"]["current_action"]["kind"] == "safety"


def test_explanatory_question_does_not_replace_reported_fish_problem():
    state = begin("fish")
    problem = "הדג נראה יבש מבחוץ ובמרכז מדדתי רק 45 מעלות. מה לעשות?"
    state = change(state, "ask", message=problem)
    state = change(state, "ask", message="למה הדג מתייבש ולמה בודקים את החום במרכז?")
    assert state["cooking_memory"]["reported_problem"] == problem
    assert "חלבוני" in state["station_protocol"]["current_action"]["text"]


def test_salty_soup_with_hard_potatoes_gets_specific_recovery():
    state = begin("soup")
    problem = "המרק מלוח מאוד ותפוח האדמה עוד קשה. איך לתקן?"
    state = change(state, "ask", message=problem)
    assert state["cooking_memory"]["reported_problem"] == problem
    assert "אל תוסיף מלח" in state["station_protocol"]["current_action"]["text"]


def test_roundtripped_step_cannot_lower_the_server_temperature_target():
    state = begin("fish")
    cook = next(s for s in state["custom_steps"] if s["minimum_temperature"] is not None)
    state = change(state, "select_step", step_id=cook["id"])
    state["custom_steps"][state["current_step"]]["minimum_temperature"] = 1
    state = change(state, "report", temperature=45)
    state = change(state, "complete")
    assert state["context"]["minimum_temperature"] == 63
    assert not state["completed_step_ids"]
