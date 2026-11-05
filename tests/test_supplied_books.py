import json

from app.coach import CoachCommand, apply_command
from app.ontology_bridge import DEFAULT_VAULT_ROOT
from app.practical_knowledge import cooking_defaults, practical_tips


def test_precise_dish_and_method_scope_without_invented_times():
    beets = cooking_defaults("סלק", "oven_roast")
    assert beets["temperature"] == 220 and beets["minutes"] == 60
    assert "program" not in beets
    assert beets["checkpoints"]
    assert cooking_defaults("סלק", "pan_sear") == {}
    assert cooking_defaults("עוף", "oven_roast") == {}
    roots = cooking_defaults("ירקות שורש", "oven_roast")
    assert roots["temperature"] == 180
    assert roots["minutes"] == 60 and "program" not in roots
    assert cooking_defaults("דלעת", "boil_simmer") == {}


def test_partial_word_does_not_match_and_notes_have_provenance():
    assert practical_tips("superonionword") == []
    tips = practical_tips("ויניגרט")
    avir = [tip for tip in tips if "SRC-AVIR-2019" in tip["source_ids"]]
    assert avir
    assert all("PDF 165" in tip["source"] and "sha256:" in tip["source"] for tip in avir)
    assert all(tip["step_keywords"] for tip in tips)


def test_defaults_flow_into_coach_and_manual_temperature_survives():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="סלק", method="oven_roast"), 1)
    assert state["intake_guidance"]["defaults"]["temperature"] == 220
    facts = {**state["intake_facts"], "oven_temperature": 190, "defaults_edited": ["temperature"]}
    state = apply_command(state, CoachCommand(action="intake", intake_facts=facts,
                                             expected_revision=state["revision"]), 2)
    assert state["intake_guidance"]["defaults"]["temperature"] == 190
    assert state["intake_guidance"]["defaults"]["minutes"] == 60
    assert "program" not in state["intake_guidance"]["defaults"]
    assert state["measured_temperature"] is None
    assert not state["completed_step_ids"]


def test_all_supplied_parts_are_audited_without_claiming_full_extraction():
    path = DEFAULT_VAULT_ROOT / "Culinary-Knowledge/09_Sources/Supplied-2026/manifest.json"
    manifest = json.loads(path.read_text(encoding="utf8"))
    assert manifest["coverage"] == "CURATED_PARTIAL"
    assert len(manifest["files"]) == 5 and len(manifest["records"]) == 16
    assert all(len(item["sha256"]) == 64 for item in manifest["files"])


def test_new_source_advice_is_idempotent_and_keeps_safety_policy():
    from app.book_knowledge import enrich_context
    from app.consultant import cooking_context

    context = cooking_context("סלק", "oven_roast")
    first = context["tips"][:]
    enrich_context(context, "סלק oven_roast")
    assert context["tips"] == first
    assert any(tip["origin"] == "OBSIDIAN_SUPPLIED" for tip in first)
    assert len(first) <= 8


def test_step_check_is_scoped_and_does_not_repeat_other_operations():
    from app.practical_knowledge import step_guidance

    assert step_guidance("סלק", "oven_roast", "קיצוץ בצל") is None
    tip = step_guidance("סלק", "oven_roast", "צלייה בתנור", checks=True)
    assert "סכין" in tip["text"] and "מים" in tip["text"]
    assert "SRC-NOSRAT-2017" in tip["source_ids"]


def test_note_change_invalidates_manifest_until_review(tmp_path, monkeypatch):
    import hashlib

    import app.practical_knowledge as module

    root = tmp_path / "Culinary-Knowledge"
    (root / "09_Sources/Supplied-2026").mkdir(parents=True)
    (root / "03_Techniques").mkdir()
    note = root / "03_Techniques/example.md"
    note.write_text("---\nid: TEST\nsource_text_checked: true\ntarget_foods: [beets]\nconditions: {}\n---\n", encoding="utf8")
    manifest = root / "09_Sources/Supplied-2026/manifest.json"
    manifest.write_text(json.dumps({"records": [{"id": "TEST", "path": "03_Techniques/example.md", "sha256": hashlib.sha256(note.read_bytes()).hexdigest()}]}))
    monkeypatch.setattr(module, "DEFAULT_VAULT_ROOT", tmp_path)
    module._index.cache_clear()
    assert module.practical_knowledge("beets")
    note.write_text(note.read_text(encoding="utf8") + "changed\n", encoding="utf8")
    assert module.practical_knowledge("beets") == []
    module._index.cache_clear()
