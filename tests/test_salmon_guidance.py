import pytest
from app.coach import CoachCommand, apply_command


def change(state, action, **kwargs):
    return apply_command(
        state, CoachCommand(action=action, expected_revision=state["revision"], **kwargs), 1001
    )


@pytest.mark.parametrize("method", ["pan_sear", "oven_roast", "steam"])
def test_salmon_choices_lead_to_specific_steps_and_continue(method):
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="סלמון"), 1000)
    paths = state["context"]["graph"]["paths"]
    assert {p["method_ref"] for p in paths} >= {"pan_sear", "oven_roast", "steam"}
    assert "עצמות" in state["messages"][-1]["text"]
    # Choose the actual method directly after the station command, without
    # requiring the obsolete generic progress question first.
    assert not any(q["id"] == "progress" for q in state["decision_questions"])
    assert len(state["station_protocol"]["blocks"]) == 6
    assert "הבחירות נשמרו" not in state["messages"][-1]["text"]
    path = next(p for p in paths if p["method_ref"] == method)
    state = change(state, "adopt_path", graph_path_id=path["id"])
    if method == "oven_roast":
        state = choose_oven_preferences(state)
    assert len(state["custom_steps"]) >= 3
    assert state["messages"][-1]["text"] == state["custom_steps"][0]["instruction"]
    state = change(state, "ask", message="מה לבדוק לפני שממשיכים?")
    assert state["current_step"] == 0
    assert state["custom_steps"][0]["successCriteria"][0] in state["messages"][-1]["text"]
    state = change(state, "complete")
    assert state["current_step"] == 1
    assert state["messages"][-1]["text"] == state["custom_steps"][1]["instruction"]
    assert state["context"]["minimum_temperature"] == 63


def test_selected_salmon_method_only_offers_matching_path():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="סלמון", method="steam"), 1000)
    assert {p["method_ref"] for p in state["context"]["graph"]["paths"]} == {"steam"}


def choose_oven_preferences(state, condition="thawed", cut="fillets", thickness="thin", flavor="lemon"):
    for key, answer in [
        ("condition", condition),
        ("cut", cut),
        ("thickness", thickness),
        ("style", "open"),
        ("flavor", flavor),
    ]:
        state = change(state, "answer", question_id="salmon_" + key, answer=answer)
    return state


def test_oven_salmon_leads_from_preferences_to_measured_doneness():
    state = apply_command(
        None, CoachCommand(action="start_custom", dish_title="דג סלומון", method="oven_roast"), 1000
    )
    assert len(state["decision_questions"]) == 5
    assert not state["custom_steps"]
    state = choose_oven_preferences(state, flavor="herbs")
    assert not state["decision_questions"]
    assert "160°C" in state["custom_steps"][0]["instruction"]
    assert "שום" in state["custom_steps"][1]["instruction"]
    assert len(state["guidance_links"]) == 2
    state = change(state, "complete")
    state = change(state, "complete")
    assert state["current_step"] == 2
    state = change(state, "complete")
    assert state["current_step"] == 2
    state = change(state, "answer", temperature=60)
    state = change(state, "complete")
    assert state["current_step"] == 2
    state = change(state, "answer", temperature=63)
    state = change(state, "complete")
    assert state["current_step"] == 3


def test_frozen_large_salmon_has_thawing_and_specific_seasoning():
    state = apply_command(
        None, CoachCommand(action="start_custom", dish_title="סלמון בתנור", method="oven_roast"), 1000
    )
    state = choose_oven_preferences(state, condition="frozen", cut="side", thickness="thick", flavor="plain")
    assert state["custom_steps"][0]["title"] == "הפשרה במקרר"
    assert "הנתח הגדול" in state["custom_steps"][2]["instruction"]
    assert "מרינדה" in state["custom_steps"][2]["instruction"]
