from copy import deepcopy

import pytest
from app.coach import CoachCommand, apply_command
from app.ingredient_safety import check_ingredients
from app.knowledge import DomainError
from conftest import chef_body
from app.food_hazards import red_bean_warning


@pytest.mark.parametrize("ingredient,allergy", [
    ("אגוזי מלך", "אגוזי מלך"), ("שקדים קלויים", "אגוזים"),
    ("טחינה גולמית", "שומשום"), ("2 tbsp tahini paste", "sesame"),
    ("פילה סלמון", "דגים"), ("Nile perch fillet", "fish"),
    ("שרימפס", "פירות ים"), ("cashews", "tree nuts"),
    ("כוס חלב", "milk"), ("עלי כוסברה", "כוסברה"),
])
def test_declared_conflicts_block_both_coach_surfaces(env, ingredient, allergy):
    command = {"action": "start_custom", "dish_title": "מנה לבחירה", "ingredients": [ingredient], "allergies": [allergy]}
    client = env["client"]
    for path, body, headers in [
        ("/v1/coach/preview", {"command": command}, {}),
        ("/v1/coach/events", command, env["headers"]),
    ]:
        response = client.post(path, json=body, headers=headers)
        assert response.status_code == 422
        assert response.json()["code"] == "ALLERGEN_CONFLICT"
    assert client.get("/v1/coach/current", headers=env["headers"]).json()["journey"] is None


def test_plan_edit_and_recipe_cannot_bypass_allergies():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="מנה", allergies=["שומשום"]), 1)
    before = deepcopy(state)
    with pytest.raises(DomainError) as error:
        apply_command(state, CoachCommand(action="update_plan", expected_revision=state["revision"], dish_title="מנה", ingredients=["טחינה גולמית"]), 2)
    assert error.value.code == "ALLERGEN_CONFLICT"
    assert state == before
    with pytest.raises(DomainError) as error:
        apply_command(state, CoachCommand(action="attach_recipe", expected_revision=state["revision"], recipe_snapshot={
            "id": "recipe", "title": "רוטב", "ingredients": ["טחינה גולמית"],
            "steps": [{"id": "mix", "text": "ערבב"}], "acquisition": "pasted",
        }), 2)
    assert error.value.code == "ALLERGEN_CONFLICT"


def test_dietary_preference_and_named_plant_alternative():
    with pytest.raises(DomainError) as error:
        check_ingredients(["קוביות בקר", "שמנת לבישול"], forbid_meat_dairy=True)
    assert error.value.code == "MEAT_DAIRY_CONFLICT"
    check_ingredients(["בקר", "חלב שיבולת שועל"], forbid_meat_dairy=True)
    check_ingredients(["בקר", "שמנת"], forbid_meat_dairy=False)
    check_ingredients(["eggplant", "חלבון אפונה"], ["eggs", "milk"])


def test_unknown_prepared_composition_requires_label_check():
    with pytest.raises(DomainError) as error:
        check_ingredients(["רוטב מוכן"], ["שומשום"])
    assert error.value.code == "INGREDIENT_COMPOSITION_UNKNOWN"


@pytest.mark.parametrize("ingredient,allergy", [("אגוזי מלך", "אגוזים"), ("טחינה גולמית", "שומשום")])
def test_grounded_chef_also_blocks_inferred_composition(env, ingredient, allergy):
    body = chef_body()
    body.update(profile={"allergies": [allergy]}, inventory=[{
        "name": ingredient, "quantity": 1, "unit": "tbsp", "verified": True, "label_verified": True,
    }])
    response = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body)
    assert response.status_code == 200
    assert response.json()["decision_type"] == "blocked"
    assert "ALLERGEN_CONFLICT" in response.json()["policy_flags"]
    assert "אל תבצע" in response.json()["station_protocol"]["blocks"][1]["text"]


def test_dried_bean_warning_is_visible_before_ordinary_advice(env):
    client = env["client"]
    state = client.post("/v1/coach/preview", json={"command": {
        "action": "start_custom", "dish_title": "תבשיל שעועית אדומה יבשה",
        "ingredients": ["שעועית אדומה יבשה"],
    }}).json()
    result = client.post("/v1/coach/preview", json={"state": state, "command": {
        "action": "ask", "expected_revision": state["revision"],
        "message": "השריתי שעועית אדומה יבשה ואני רוצה לבשל בסיר איטי על חום נמוך. זה בטוח?",
    }})
    assert result.status_code == 200
    protocol = result.json()["station_protocol"]
    assert "השריה לבדה אינה מספיקה" in protocol["blocks"][0]["text"]
    assert "30 דקות" in protocol["blocks"][0]["text"]
    assert "אל תבצע" in protocol["blocks"][1]["text"]
    assert any("fda.gov" in resource["url"] for resource in protocol["blocks"][5]["resources"])


@pytest.mark.parametrize("name", ["שעועית אדומה משומרת", "canned red kidney beans", "שעועית אדומה מבושלת מראש"])
def test_cooked_bean_controls_do_not_get_dried_bean_instructions(name):
    assert red_bean_warning([name]) is None


def test_unspecified_beans_request_state_instead_of_assuming_cooked():
    assert "יבשה, משומרת" in red_bean_warning(["שעועית אדומה"])["question"]
    assert red_bean_warning(["עדשים ירוקות"]) is None
