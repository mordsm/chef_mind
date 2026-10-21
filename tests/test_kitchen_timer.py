from app.coach import CoachCommand, apply_command


def command(state, action, **kwargs):
    return apply_command(
        state, CoachCommand(action=action, expected_revision=state["revision"], **kwargs), now=1000
    )


def test_cancel_timer_keeps_work_active():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="קורקבנים"), now=1000)
    state = command(state, "timer", seconds=300)
    assert state["timer_deadline"] == 1300
    state = command(state, "timer_cancel")
    assert state["status"] == "active"
    assert state["timer_deadline"] is None and state["check_due_at"] is None
    assert "בוטלה" in state["messages"][-1]["text"]


def test_cancel_paused_timer_does_not_restart_on_resume():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="קורקבנים"), now=1000)
    state = command(state, "timer", seconds=300)
    state = command(state, "pause")
    assert state["paused_remaining"] == 300
    state = command(state, "timer_cancel")
    assert state["status"] == "paused" and state["paused_remaining"] is None
    state = command(state, "resume")
    assert state["timer_deadline"] is None


def test_guided_timer_can_be_cancelled():
    state = apply_command(None, CoachCommand(action="start", recipe_id="shakshuka"), now=1000)
    state = command(state, "timer", seconds=300)
    state = command(state, "timer_cancel")
    assert state["timer_deadline"] is None and state["status"] == "active"
