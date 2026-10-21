import pytest
from app.coach import CoachCommand, apply_command
from app.culinary_context import dish_context
from app.knowledge import DomainError


def change(state, action, now=1000, **kwargs):
    return apply_command(
        state, CoachCommand(action=action, expected_revision=state["revision"], **kwargs), now
    )


@pytest.mark.parametrize(
    "dish,family",
    [
        ("כנפי הודו", "poultry"),
        ("דג ברוטב", "fish"),
        ("אורז עם ירקות", "grains"),
        ("מרק ירקות", "soup"),
        ("פסטה עם עוף", "pasta"),
        ("מנה לא מזוהה", "general"),
    ],
)
def test_context_works_without_a_named_recipe(dish, family):
    state = apply_command(None, CoachCommand(action="start_custom", dish_title=dish), 1000)
    assert state["context"]["family"] == family
    assert state["custom_steps"] == [] and state["workflow"] == "user"
    assert state["context"]["tips"] and state["context"]["questions"]


def test_mixed_dish_still_gets_poultry_safety_without_becoming_roast_chicken():
    context = dish_context("פסטה עם עוף")
    assert context["family"] == "pasta" and context["minimum_temperature"] == 74
    assert dish_context("פסטה ללא עוף")["minimum_temperature"] is None


def test_user_owns_plan_and_reports_do_not_advance_it():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="כנפי הודו"), 1000)
    state = change(state, "add_step", step_title="תיבול")
    first_id = state["custom_steps"][0]["id"]
    state = change(state, "add_step", step_title="צלייה")
    second_id = state["custom_steps"][1]["id"]
    state = change(state, "report", message="הכנסתי לתנור")
    assert len(state["custom_steps"]) == 2 and state["completed_step_ids"] == []
    state = change(state, "move_step", step_id=second_id, target_index=0)
    assert state["custom_steps"][state["current_step"]]["id"] == first_id
    state = change(
        state, "edit_step", step_id=first_id, step_title="התיבול שלי", step_instruction="לפי בחירתי"
    )
    assert state["custom_steps"][1]["instruction"] == "לפי בחירתי"
    assert state["custom_steps"][1]["source"] == "USER_PROVIDED"
    state = change(state, "complete")
    assert state["completed_step_ids"] == [first_id] and state["status"] == "active"
    state = change(state, "remove_step", step_id=second_id)
    assert len(state["custom_steps"]) == 1


def test_recovery_is_contextual_and_debrief_does_not_invent_success():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="פסטה"), 1000)
    state = change(state, "ask", message="הרוטב סמיך מדי")
    assert "מי הבישול" in state["messages"][-1]["text"]
    assert state["issues"] == ["סמיכות הרוטב"]
    state = change(state, "finish")
    assert state["status"] == "completed"
    assert any("לא דווח בהכרח שטופלו" in item for item in state["completion_summary"])


def test_user_can_end_work_but_not_get_unmeasured_safety_clearance():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="כנפי הודו"), 1000)
    state = change(state, "report", message="העוף נראה מוכן")
    assert "מדידה" in state["messages"][-1]["text"]
    state = change(state, "finish")
    assert any("אינו אישור" in text for text in state["completion_summary"])


def test_measurements_only_from_explicit_numeric_report_not_incidental_text():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="כנפי הודו"), 1000)
    state = change(state, "report", message="התנור על 180 מעלות; לא מדדתי 74 מעלות")
    assert state["measured_temperature"] is None
    state = change(state, "report", temperature=73)
    assert "נמוכה" in state["messages"][-1]["text"]
    state = change(state, "report", temperature=74)
    assert "עומדת בסף" in state["messages"][-1]["text"]


def test_modes_and_idle_checks_are_deduplicated_without_plan_changes():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="אורז"), 1000)
    assert change(state, "check_in", now=1299) == state
    state = change(state, "check_in", now=1300)
    assert "idle" in state["asked"] and state["custom_steps"] == []
    assert change(state, "check_in", now=1301) == state
    state = change(state, "mode", now=1400, mode="consultant")
    assert state["checkin_seconds"] == 600
    assert change(state, "check_in", now=1999) == state


def test_safety_hold_survives_user_control_but_user_can_stop():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="בצל"), 1000)
    state = change(state, "report", message="המחבת עולה באש")
    with pytest.raises(DomainError):
        change(state, "resume")
    state = change(state, "finish")
    assert any("סיכון" in text for text in state["completion_summary"])


def test_custom_journey_is_persisted_and_owner_scoped(env):
    client, headers = env["client"], env["headers"]
    state = client.post(
        "/v1/coach/events", headers=headers, json={"action": "start_custom", "dish_title": "כנפי הודו"}
    ).json()
    assert state["workflow"] == "user"
    result = client.post(
        "/v1/coach/events",
        headers=headers,
        json={
            "action": "add_step",
            "step_title": "תיבול",
            "journey_id": state["id"],
            "expected_revision": state["revision"],
        },
    )
    assert result.status_code == 200
    assert (
        client.get("/v1/coach/current", headers=headers).json()["journey"]["custom_steps"][0]["title"]
        == "תיבול"
    )
    assert client.get("/v1/coach/current", headers=env["other"]).json()["journey"] is None


def test_recipe_edits_preserve_original_and_actions_but_reset_measurement():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="כנפי הודו"), 1000)
    state = change(state, "add_step", step_title="הפעולה שלי")
    state = change(state, "report", temperature=74)
    state = change(state, "update_plan", dish_title="הודו עם ירקות", ingredients=["הודו", "גזר"])
    assert state["original_dish_title"] == "כנפי הודו"
    assert state["custom_steps"][0]["title"] == "הפעולה שלי"
    assert state["measured_temperature"] is None


def test_known_ingredient_avoidance_is_retained_in_custom_work():
    with pytest.raises(DomainError) as result:
        apply_command(
            None,
            CoachCommand(action="start_custom", dish_title="פסטה", ingredients=["חלב"], allergies=["milk"]),
            1000,
        )
    assert result.value.code == "ALLERGEN_CONFLICT"


def test_turkey_wings_have_specific_reusable_knowledge():
    context = dish_context("כנפי הודו", "תנור")
    assert context["family"] == "poultry"
    assert any("butterball.com" in tip["source"] for tip in context["tips"])
