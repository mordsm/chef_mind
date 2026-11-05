from app.book_knowledge import book_tips, enrich_context
from app.coach import CoachCommand, apply_command
from app.consultant import cooking_context
import pytest


def test_gizzard_context_keeps_safety_and_adds_attributed_book_explanation():
    context = cooking_context("קורקבנים", "boil_simmer")
    assert any(tip["origin"] == "SAFETY_POLICY" for tip in context["tips"])
    tips = [tip for tip in context["tips"] if tip["origin"] == "OBSIDIAN_FOODLAB"]
    assert tips and len(context["tips"]) <= 8
    assert all("SRC-FOODLAB-2015" in tip["source_ids"] and tip["practical"] for tip in tips)
    assert all("sha256:" in tip["source"] for tip in tips)


def test_unrelated_query_does_not_receive_book_advice():
    assert book_tips("zzzzzzzzzzzzzzzzz") == []


@pytest.mark.parametrize("query", ["fish poaching", "שליקת דגים"])
def test_fish_retrieval_reads_existing_legacy_note_without_egg_advice(query):
    tips = book_tips(query, limit=6)
    fish = next(tip for tip in tips if tip.get("knowledge_id") == "TEC-FISH-002")
    assert "SRC-MCGEE-2004" in fish["source_ids"]
    assert len(fish["revision_sha256"]) == 64
    assert fish["usage"] == "retrieved_background_not_approved_action"
    assert not any("TEC-EGG-002" in tip["source_ids"] for tip in tips)
    assert not any("שליקת ביצים" in tip["title"] for tip in tips)


def test_enrichment_preserves_existing_tips_and_is_idempotent():
    context = cooking_context("קורקבנים", "boil_simmer")
    originals = [
        tip for tip in context["tips"] if tip["origin"] not in ("OBSIDIAN_MCGEE", "OBSIDIAN_FOODLAB")
    ]
    enrich_context(context, "קורקבנים")
    first = context["tips"][:]
    enrich_context(context, "קורקבנים")
    assert context["tips"] == first
    assert all(tip in first for tip in originals)


def test_report_refreshes_book_context_without_changing_user_plan():
    state = apply_command(
        None, CoachCommand(action="start_custom", dish_title="קורקבנים", method="boil_simmer"), 1000
    )
    state = apply_command(
        state, CoachCommand(action="report", message="הנוזל רתח", expected_revision=state["revision"]), 1001
    )
    assert any(tip["practical"] for tip in state["context"]["tips"])
    assert "90–120" in state["messages"][-1]["text"]
    assert not state["completed_step_ids"]


def test_foodlab_claims_available_with_epub_provenance_and_limits():
    tips = book_tips("חרדל ויניגרט הפרדה")
    tips = [tip for tip in tips if tip["origin"] == "OBSIDIAN_FOODLAB"]
    assert tips
    assert all("SRC-FOODLAB-2015" in tip["source_ids"] for tip in tips)
    assert all("text/part" in tip["source"] and "פסקה" in tip["source"] for tip in tips)
    assert all("ללא אימות מדעי עצמאי" in tip["source"] for tip in tips)
    assert all("ללא אימות מדעי עצמאי" not in tip["text"] for tip in tips)


def test_both_books_and_existing_safety_remain_in_context():
    context = cooking_context("קורקבנים", "boil_simmer")
    origins = {tip["origin"] for tip in context["tips"]}
    assert {"SAFETY_POLICY", "OBSIDIAN_FOODLAB"} <= origins
    assert len(context["tips"]) <= 8


def test_chef_answer_uses_foodlab_evidence():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="סלט"), 1000)
    state = apply_command(
        state,
        CoachCommand(
            action="ask", message="למה חרדל עוזר לויניגרט לא להיפרד?", expected_revision=state["revision"]
        ),
        1001,
    )
    assert "חרדל" in state["messages"][-1]["text"]
    assert "פסקה" not in state["messages"][-1]["text"]


def test_supplied_mcgee_ranges_have_printed_full_and_split_page_provenance():
    tips = book_tips("קקאו טבעי סודה")
    tips = [tip for tip in tips if tip["source_ids"][1].startswith(("EVD-MCG-RNG-", "RUL-MCG-RNG-"))]
    assert tips
    assert all("PDF" in tip["source"] and "עמוד בחלק" in tip["source"] for tip in tips)
    assert all(".pdf" in tip["source"] and "ללא אימות מדעי עצמאי" in tip["source"] for tip in tips)


def test_chef_uses_new_mcgee_cocoa_evidence():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="עוגת קקאו"), 1000)
    state = apply_command(
        state,
        CoachCommand(
            action="ask",
            message="האם להחליף קקאו טבעי בקקאו בסיסי כשיש סודה?",
            expected_revision=state["revision"],
        ),
        1001,
    )
    assert "קקאו" in state["messages"][-1]["text"]
    assert "PDF" not in state["messages"][-1]["text"]


def test_vegetable_guidance_has_a_test_instead_of_vague_limits():
    tips = book_tips("חומציות וריכוך ירקות רוטב עגבניות")
    tip = next(t for t in tips if t["source_ids"][1] == "EVD-MCG-RNG-CH05-002")
    assert "מזלג" in tip["text"]
    assert "סנן" in tip["text"]
    assert "לא מתכון שמופיע בספר" in tip["text"]
    assert "מינון סודה אוטומטי" not in tip["text"]


def test_dish_cards_do_not_match_other_families_through_generic_softening_words():
    context = cooking_context("קורקבנים ברוטב", "boil_simmer")
    enrich_context(context, "קורקבנים עדיין קשים רוצים ריכוך")
    cards = [tip for tip in context["tips"] if tip["origin"].startswith("OBSIDIAN_")]
    assert cards and all(tip["practical"] for tip in cards)
    assert all("עגבניות" not in tip["text"] and "מרינדה" not in tip["text"] for tip in cards)
    assert all("הקורקבנים" in tip["text"] for tip in cards)


def test_vegetable_acid_guidance_requires_vegetables_and_tomatoes_in_dish():
    plain = cooking_context("גזר מאודה", "steam")
    assert not any("עגבניות" in tip["text"] for tip in plain["tips"])
    tomato = cooking_context("ירקות ברוטב עגבניות", "boil_simmer")
    cards = [tip for tip in tomato["tips"] if tip["practical"]]
    assert cards and "מזלג" in cards[0]["text"]
    assert "הספר מציע" not in cards[0]["text"]
