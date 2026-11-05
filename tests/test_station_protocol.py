from copy import deepcopy

import pytest
import yaml
from app.coach import CoachCommand, JourneyState, apply_command
from app.method_policy import effective_policy, recommendations
from app.station_protocol import TITLES, build_protocol, configuration
from conftest import chef_body


@pytest.fixture
def approved_fish(monkeypatch):
    cfg = deepcopy(configuration())
    cfg["fish_safety"].update(approval_status="APPROVED", core_c=63, hold_seconds=15)
    monkeypatch.setattr("app.station_protocol.configuration", lambda: deepcopy(cfg))
    return cfg


def assert_contract(protocol):
    assert [block["title"] for block in protocol["blocks"]] == TITLES
    assert all(block["text"] for block in protocol["blocks"])
    assert "Knowledge Base Extension Needed" in protocol["blocks"][5]["text"]
    assert "McGee" in protocol["blocks"][5]["text"]
    assert "פרק" in protocol["blocks"][5]["text"]
    assert "[[" in protocol["blocks"][4]["text"]
    assert "#culinary/" in protocol["blocks"][4]["text"]
    assert protocol["text"].index("הפרט הבא") > protocol["text"].index(TITLES[-1])


def test_nile_perch_without_model_or_method_profile(approved_fish):
    policy = {"default_reason": "אין פרופיל; נדרש בירור שיטה", "profiles": []}
    state = apply_command(
        None,
        CoachCommand(action="start_custom", dish_title="נסיכת הנילוס"),
        1000,
        method_policy=policy,
        recognition={"status": "unavailable"},
    )
    assert not state["method_recommendations"]["profile_id"]
    assert state["intake_guidance"]["family"] == "fish"
    for command in [
        CoachCommand(action="intake", expected_revision=state["revision"], intake_facts={"family": "fish"}),
        None,
    ]:
        if command is None:
            command = CoachCommand(
                action="ask", expected_revision=state["revision"], message="איך להכין את הדג?"
            )
        state = apply_command(
            JourneyState.model_validate(state).model_dump(), command, 1001, method_policy=policy
        )
        protocol = state["station_protocol"]
        assert_contract(protocol)
        assert "63°C" in protocol["blocks"][1]["text"]
        assert "15 שניות" in protocol["blocks"][1]["text"]
        assert "70–80°C" in protocol["blocks"][1]["text"]
        assert "geosmin" in protocol["blocks"][2]["text"]
        assert "2-MIB" in protocol["blocks"][2]["text"]
        assert "Chenin Blanc" in protocol["blocks"][3]["text"]
        assert "Anjou" in protocol["blocks"][3]["text"]
        assert "נסיכת הנילוס" in protocol["next_question"]
        assert "עובי" in protocol["next_question"]
        assert protocol["knowledge_gap_flagged"]


@pytest.mark.parametrize(
    "title,family",
    [
        ("דג מים מתוקים לא מוכר", "fish"),
        ("ירק לא מוכר", "vegetables"),
        ("טכניקה לא מוכרת", ""),
        ("תבשיל בשר", "meat"),
    ],
)
def test_general_fallback_and_export(title, family):
    protocol = build_protocol(title, family=family, model_status="unavailable")
    assert_contract(protocol)
    header = yaml.safe_load(protocol["obsidian_markdown"].split("---", 2)[1])
    assert header["type"] == "culinary-station-log"
    assert header["knowledge_gap_flagged"] is True
    assert header["links"] == protocol["wikilinks"]
    assert header["tags"] == protocol["tags"]
    assert header["recommended_reading"]["chapter"]


def test_pending_safety_does_not_publish_unapproved_core(monkeypatch):
    cfg = deepcopy(configuration())
    cfg["fish_safety"]["approval_status"] = "PENDING_OWNER_APPROVAL"
    monkeypatch.setattr("app.station_protocol.configuration", lambda: cfg)
    protocol = build_protocol("נסיכת הנילוס")
    assert "ממתין לאישור" in protocol["blocks"][1]["text"]
    assert "אל תחמם" in protocol["blocks"][1]["text"]


@pytest.mark.parametrize(
    "kwargs", [{"blocked": True}, {"method_warning": "שיטה חסומה"}, {"facts": {"family": "meat"}}]
)
def test_safety_holds_override_cooking(approved_fish, kwargs):
    protocol = build_protocol("נסיכת הנילוס", **kwargs)
    assert "עצור" in protocol["blocks"][0]["text"]
    assert "אל תבצע" in protocol["blocks"][1]["text"]
    assert "63°C" not in protocol["blocks"][1]["text"]
    assert "אל תטעם" in protocol["blocks"][3]["text"]


@pytest.mark.parametrize("cut", ["דג ממולא", "דג טחון", "נתח קפוא"])
def test_intact_fish_profile_does_not_cover_other_processes(approved_fish, cut):
    protocol = build_protocol("נסיכת הנילוס", facts={"cut": cut})
    assert "הפרוטוקול אינו מתאים" in protocol["blocks"][1]["text"]
    assert "63°C" not in protocol["blocks"][1]["text"]


def test_user_method_is_not_silently_replaced(approved_fish):
    protocol = build_protocol("סלמון", family="fish", method="oven_roast")
    assert "נשמרה" in protocol["blocks"][1]["text"]
    assert "שלוק" not in protocol["blocks"][1]["text"]


def test_nile_perch_method_registry():
    options = recommendations("נסיכת הנילוס", [], effective_policy()["policy"])
    assert options["profile_id"] == "engine_nile_perch"
    assert {item["id"] for item in options["allowed"]} == {"boil_simmer", "steam"}
    assert {"deep_fry", "grill_direct"} <= {item["id"] for item in options["blocked"]}


def test_missing_station_profile_still_resolves_ingredient_family(approved_fish):
    approved_fish["profiles"] = []
    protocol = build_protocol("נסיכת הנילוס", model_status="disabled")
    assert protocol["profile_id"] is None
    assert protocol["family"] == "fish"
    assert_contract(protocol)
    assert "63°C" in protocol["blocks"][1]["text"]
    assert "Fish Collagen" in protocol["blocks"][4]["text"]


def test_fish_allergy_applies_even_without_inventory(approved_fish):
    protocol = build_protocol("נסיכת הנילוס", allergies=["דגים"])
    assert "אל תכין" in protocol["blocks"][0]["text"]
    assert "אל תבצע" in protocol["blocks"][1]["text"]


def test_both_api_surfaces_and_persistence(env, approved_fish):
    client = env["client"]
    preview = client.post(
        "/v1/coach/preview", json={"command": {"action": "start_custom", "dish_title": "נסיכת הנילוס"}}
    )
    assert preview.status_code == 200
    assert_contract(preview.json()["station_protocol"])
    body = chef_body()
    body.update(message="נסיכת הנילוס", state={"current_goal": "נסיכת הנילוס"})
    response = client.post("/v1/chef/respond", headers=env["headers"], json=body)
    assert response.status_code == 200
    assert_contract(response.json()["station_protocol"])
    assert response.json()["citations"] == []  # Editorial protocol is not fabricated approved evidence.
    started = client.post(
        "/v1/coach/events",
        headers=env["headers"],
        json={"action": "start_custom", "dish_title": "נסיכת הנילוס"},
    )
    assert started.status_code == 200
    saved = client.get("/v1/coach/current", headers=env["headers"])
    assert saved.status_code == 200
    assert_contract(saved.json()["journey"]["station_protocol"])


def test_api_blocked_decision_cannot_become_a_fish_cooking_instruction(env, approved_fish):
    body = chef_body()
    body.update(
        message="נסיכת הנילוס", state={"current_goal": "נסיכת הנילוס"}, profile={"allergies": ["fish"]}
    )
    body["inventory"] = [
        {"name": "fish", "quantity": 1, "unit": "kg", "verified": True, "allergens": ["fish"]}
    ]
    response = env["client"].post("/v1/chef/respond", headers=env["headers"], json=body)
    assert response.status_code == 200
    decision = response.json()
    assert decision["decision_type"] == "blocked"
    assert "אל תבצע" in decision["station_protocol"]["blocks"][1]["text"]
