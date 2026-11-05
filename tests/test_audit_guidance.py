from app.coach import CoachCommand, apply_command


def test_burning_report_changes_foreground_without_opening_science():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="תבשיל בקר", ingredients=["בקר", "בצל"]), 1)
    state = apply_command(state, CoachCommand(action="ask", expected_revision=state["revision"], message="הבצל נשרף ונעשה שחור. איך להמשיך?"), 2)
    protocol = state["station_protocol"]
    assert "אל תערבב חלקים שרופים" in protocol["current_action"]["text"]
    assert protocol["current_action"]["kind"] == "warning"
    assert "אל תערבב חלקים שרופים" not in protocol["blocks"][2]["text"]


def test_fire_and_dried_beans_override_other_foreground_answers():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="שעועית אדומה יבשה"), 1)
    assert state["station_protocol"]["current_action"]["kind"] == "safety"
    assert "השריה לבדה" in state["station_protocol"]["current_action"]["text"]
