import pytest
from app.coach import RECIPES, CoachCommand, SmartStep, apply_command
from app.knowledge import DomainError


def update(state, action, now=1000, **extra):
    return apply_command(
        state, CoachCommand(action=action, expected_revision=state["revision"], **extra), now
    )


def test_time_and_clicking_done_do_not_complete_unvalidated_steps():
    state = apply_command(None, CoachCommand(action="start"), 1000)
    result = update(state, "complete", now=10000)
    assert result["current_step"] == 0 and result["stage_valid"] is False
    result = update(result, "answer", answer="ready")
    result = update(result, "complete")
    assert result["current_step"] == 1
    result = update(result, "answer", answer="white")
    result = update(result, "complete")
    assert result["current_step"] == 1
    result = update(result, "answer", answer="golden")
    assert result["stage_valid"]
    result = update(result, "answer", answer="dark")
    assert not result["stage_valid"]  # A worse report invalidates an earlier success.


def test_check_ins_are_due_deduplicated_and_never_advance():
    state = apply_command(None, CoachCommand(action="start"), 1000)
    state = update(state, "timer", seconds=30)
    before = update(state, "check_in", now=1029)
    assert before == state
    due = update(state, "check_in", now=1030)
    assert due["current_step"] == state["current_step"] and "time" in due["asked"]
    assert len(due["messages"]) == len(state["messages"]) + 1
    assert update(due, "check_in", now=1031) == due
    idle = update(due, "check_in", now=1180)
    assert "idle" in idle["asked"]
    assert update(idle, "check_in", now=1181) == idle


def test_pause_freezes_timer_resume_rebases_it():
    state = apply_command(None, CoachCommand(action="start"), 1000)
    state = update(state, "timer", seconds=60)
    state = update(state, "pause", now=1020)
    assert state["timer_deadline"] is None and state["paused_remaining"] == 40
    with pytest.raises(DomainError):
        update(state, "answer", answer="ready")
    state = update(state, "resume", now=2000)
    assert state["timer_deadline"] == 2040


def test_chicken_requires_measured_temperature_and_personality_cannot_override_it():
    state = apply_command(None, CoachCommand(action="start", recipe_id="chicken"), 1000)
    for _ in range(2):
        state = update(state, "answer", answer="ready")
        state = update(state, "complete")
    with pytest.raises(DomainError):
        update(state, "answer", answer="ready")
    state = update(state, "answer", temperature=73)
    state = update(state, "personality", chefPersonality="tough")
    assert not state["stage_valid"]
    assert update(state, "complete")["current_step"] == 2
    state = update(state, "answer", temperature=74)
    assert update(state, "complete")["current_step"] == 3


def test_templates_have_all_smart_step_layers():
    for recipe in RECIPES.values():
        for step in recipe["steps"]:
            SmartStep.model_validate(step)
            assert (
                step["recoveryInstructions"]
                and step["successCriteria"]
                and step["source"].startswith("https:")
            )


def test_persistence_owner_isolation_stale_revision_and_wrong_journey(env):
    client = env["client"]
    assert client.get("/v1/coach/recipes").status_code == 200
    assert client.get("/v1/coach/current").status_code == 401
    assert client.post("/v1/coach/events", json={"action": "start"}).status_code == 401
    state = client.post("/v1/coach/events", headers=env["headers"], json={"action": "start"}).json()
    assert client.get("/v1/coach/current", headers=env["headers"]).json()["journey"] == state
    assert client.get("/v1/coach/current", headers=env["other"]).json()["journey"] is None
    body = {
        "action": "answer",
        "answer": "ready",
        "expected_revision": state["revision"],
        "journey_id": state["id"],
    }
    assert (
        client.post(
            "/v1/coach/events", headers=env["headers"], json={**body, "journey_id": "other"}
        ).status_code
        == 409
    )
    assert client.post("/v1/coach/events", headers=env["headers"], json=body).status_code == 200
    assert client.post("/v1/coach/events", headers=env["headers"], json=body).status_code == 409


def test_guest_preview_does_not_create_private_records(env):
    client = env["client"]
    response = client.post("/v1/coach/preview", json={"command": {"action": "start"}})
    assert response.status_code == 200
    assert client.get("/v1/coach/current", headers=env["headers"]).json()["journey"] is None


def test_finish_requires_validation_and_stops_timers():
    state = apply_command(None, CoachCommand(action="start"), 1000)
    for index in range(len(RECIPES["shakshuka"]["steps"])):
        state = update(state, "answer", answer="golden" if index == 1 else "ready")
        state = update(state, "complete")
    assert state["status"] == "completed" and state["timer_deadline"] is None
    with pytest.raises(DomainError):
        update(state, "complete")


def test_hazard_question_interrupts_coaching():
    state = apply_command(None, CoachCommand(action="start"), 1000)
    state = update(state, "ask", message="המחבת עולה באש")
    assert state["status"] == "paused" and not state["stage_valid"]
    with pytest.raises(DomainError):
        update(state, "resume")
    state = update(state, "resume", hazard_resolved=True)
    assert state["status"] == "active" and not state["safety_hold"]


def test_known_allergen_conflict_blocks_start():
    with pytest.raises(DomainError) as result:
        apply_command(None, CoachCommand(action="start", recipe_id="shakshuka", allergies=["ביצים"]), 1000)
    assert result.value.code == "ALLERGEN_CONFLICT"
