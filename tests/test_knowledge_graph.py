import pytest
from app.coach import CoachCommand, apply_command
from app.knowledge import DomainError
from app.knowledge_graph import audit_graph, dietary_paths, graph, graph_context, minimum_for


def start(title="פילה סלמון", method="צריבה במחבת"):
    return apply_command(None, CoachCommand(action="start_custom", dish_title=title, method=method), 1000)


def change(state, action, **kwargs):
    return apply_command(
        state, CoachCommand(action=action, expected_revision=state["revision"], **kwargs), 1100
    )


def test_graph_coverage_and_reference_integrity():
    data = graph()
    assert len(data["ingredients"]) == 75
    assert len(data["methods"]) == 10
    assert len(data["paths"]) == 20
    assert len(data["raw"]["preparations"]) == 5
    assert len(data["sha256"]) == 64
    for path in data["paths"]:
        assert path["ingredient_ref"] in data["ingredients"]
        assert path["method_ref"] in data["methods"]
        assert path["suggestions"]
    assert len(audit_graph()["safety_changes"]) == 29


def test_texture_targets_are_not_safety_thresholds():
    assert minimum_for("duck_breast") == (74, 0)
    assert minimum_for("beef_ribeye") == (63, 180)
    assert minimum_for("fish_salmon") == (63, 0)
    assert all(node["tip"] for node in graph()["ingredients"].values())


def test_graph_advice_does_not_impose_steps_or_infer_observations():
    state = start()
    assert state["custom_steps"] == []
    context = state["context"]["graph"]
    assert context["ingredients"] and context["method"]["id"] == "pan_sear"
    rule = context["method"]["observations"][0]
    state = change(state, "report", observation=rule["id"])
    assert state["messages"][-1]["text"] == rule["message"]
    assert rule["source_id"] in state["applied_graph_rules"]
    assert state["completed_step_ids"] == []
    with pytest.raises(DomainError):
        change(state, "report", observation="nonexistent_sensor")


def test_optional_path_requires_relevant_explicit_choice():
    state = start()
    paths = [path for path in state["context"]["graph"]["paths"] if path["selectable"]]
    assert paths
    state = change(state, "adopt_path", graph_path_id=paths[0]["id"])
    assert len(state["custom_steps"]) == len(paths[0]["detailed_steps"])
    assert all(item["source"].startswith("USER_GRAPH_ADAPTED:") for item in state["custom_steps"])
    with pytest.raises(DomainError):
        change(state, "adopt_path", graph_path_id="unknown")


def test_dietary_and_unvalidated_process_restrictions():
    data = graph()
    context = {"paths": data["paths"]}
    filtered = dietary_paths(context, ["milk"], True)
    for path in filtered["paths"]:
        if "milk" in path["introduced_allergens"] or path["method_ref"] in ("raw_cure", "sous_vide"):
            assert not path["selectable"]
    assert graph_context("פסטה ללא עוף")["minimum_temperature"] is None
    assert all(not node["id"].startswith("chicken_") for node in graph_context("פסטה ללא עוף")["ingredients"])


def test_reported_rest_is_separate_from_core_temperature():
    state = start("אנטריקוט")
    state = change(state, "report", rest_seconds=180)
    assert state["measured_rest_seconds"] == 180
    assert state["measured_temperature"] is None
    state = change(state, "update_plan", dish_title="כנפי הודו")
    assert state["measured_rest_seconds"] is None


def test_safety_observation_pauses_and_cannot_be_cleared_by_time():
    state = start()
    rule = next(
        rule for rule in state["context"]["graph"]["method"]["observations"] if rule["severity"] == "safety"
    )
    state = change(state, "report", observation=rule["id"])
    assert state["status"] == "paused" and state["safety_hold"]
    assert state["timer_deadline"] is None
    with pytest.raises(DomainError):
        change(state, "resume")
    assert change(state, "resume", hazard_resolved=True)["status"] == "active"


def test_domain_inheritance_and_path_merging():
    from app.culinary_domain import domain_graph

    domain = domain_graph()
    assert len(domain["inheritance"]) == 23
    assert len(domain["raw"]["archetypes"]) == 16
    assert len(graph()["paths"]) == 20
    assert all(path["detailed_steps"] and path["domain_source_id"] for path in graph()["paths"])
    salmon = graph()["ingredients"]["fish_salmon_fillet"]
    assert salmon["archetype_ref"] == "fish_fatty_steak"
    assert salmon["minimum_temperature"] == 63
    assert salmon["inherited_advice"]
    assert graph()["ingredients"]["legume_chickpeas"]["archetype_ref"] == "legume_dry_dense"
    assert graph()["ingredients"]["fish_sea_bass_whole"]["archetype_ref"] == "fish_delicate_white"


def test_adopted_domain_steps_are_editable_and_have_no_original_timers():
    state = start()
    path = next(path for path in state["context"]["graph"]["paths"] if path["selectable"])
    state = change(state, "adopt_path", graph_path_id=path["id"])
    first = state["custom_steps"][0]
    assert first["next_step_prep"] and first["why"]
    assert first["estimated_seconds"] == 0 and state["timer_deadline"] is None
    assert first["successCriteria"] == path["detailed_steps"][0]["successCriteria"]
    state = change(state, "edit_step", step_id=first["id"], step_title="הפעולה שלי")
    assert state["custom_steps"][0]["title"] == "הפעולה שלי"


def test_sous_vide_temperature_report_is_not_process_validation():
    state = start("פילה בקר", "סו־וויד")
    state = change(state, "report", temperature=70)
    assert "אינה מאמתת תהליך" in state["messages"][-1]["text"]
    assert state["custom_steps"] == []
