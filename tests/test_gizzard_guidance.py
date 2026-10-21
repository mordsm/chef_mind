import pytest
from app.coach import CoachCommand, apply_command
from app.knowledge_graph import graph_context


@pytest.mark.parametrize("title", ["קוקבנים", "קורקבנים", "קורקבן", "gizzards"])
def test_gizzard_start_provides_advice_safety_and_questions(title):
    state = apply_command(None, CoachCommand(action="start_custom", dish_title=title), now=1000)
    context = state["context"]
    assert context["identified"]
    assert context["minimum_temperature"] == 74
    assert context["graph"]["ingredients"][0]["id"] == "chicken_giblets"
    opening = state["messages"][-1]["text"]
    assert "מנוקים" in opening
    assert "בנוזל" in opening
    assert "74" in opening
    assert "סיר לחץ" in opening
    assert "ברוטב" in opening
    assert "האם מדובר בקורקבן או בכבד" not in opening
    assert state["custom_steps"] == []  # Advice does not silently change the cook's plan.


def test_gizzards_do_not_override_explicit_negation_or_liver_identity():
    assert graph_context("מרק ללא קוקבנים")["minimum_temperature"] is None
    liver = apply_command(None, CoachCommand(action="start_custom", dish_title="כבד עוף"), now=1000)
    assert "זוהו קורקבנים" not in liver["messages"][-1]["text"]
