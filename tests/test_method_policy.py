import pytest
import yaml
from app.coach import CoachCommand, apply_command
from app.knowledge import DomainError
from app.method_policy import effective_policy, recommendations


@pytest.mark.parametrize("title", ["קורקבנים", "קוקבנים", "gizzards", "הקורקבנים"])
def test_gizzards_have_only_configured_recommendations(title):
    result = recommendations(title, [], effective_policy()["policy"])
    assert {item["id"] for item in result["allowed"]} == {"braise", "boil_simmer"}
    assert next(item for item in result["blocked"] if item["id"] == "oven_roast")["reason"]


def test_server_blocks_explicit_and_inferred_oven_and_plan_update():
    for title, method in [("קוקבנים", "תנור"), ("קורקבנים בתנור", ""), ("קורקבנים", "oven_roast")]:
        with pytest.raises(DomainError) as error:
            apply_command(
                None, CoachCommand(action="start_custom", dish_title=title, method=method), now=1000
            )
        assert error.value.code == "METHOD_NOT_RECOMMENDED"
        assert "צלייה בתנור" in error.value.message
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="קוקבנים"), now=1000)
    with pytest.raises(DomainError):
        apply_command(
            state,
            CoachCommand(action="update_plan", dish_title="קוקבנים", method="תנור", expected_revision=1),
        )
    with pytest.raises(DomainError):
        apply_command(state, CoachCommand(action="answer", message="מחבת", expected_revision=1))
    assert state["method"] == "" and state["revision"] == 1
    methods = next(q for q in state["decision_questions"] if q["id"] == "method")
    assert "pan" not in {option["id"] for option in methods["options"]}


def test_unknown_dish_does_not_receive_an_unrestricted_method_list():
    result = recommendations("unknownzzdish", [], effective_policy()["policy"])
    assert result["allowed"] == [] and result["reason"]


def test_report_on_legacy_unsupported_method_is_acknowledged():
    state = apply_command(None, CoachCommand(action="start_custom", dish_title="קוקבנים"), now=1000)
    state["method"] = "צלייה בתנור"
    changed = apply_command(
        state, CoachCommand(action="report", message="הוספתי נוזלים", expected_revision=1), now=1001
    )
    assert changed["method_warning"]
    assert changed["report_count"] == 1
    assert "הדיווח התקבל: הוספתי נוזלים" in changed["messages"][-1]["text"]


def test_reviewed_private_configuration_is_enforced_and_scoped(env):
    client, headers = env["client"], env["headers"]
    default = client.get("/v1/coach/method-policy/template").json()
    data = yaml.safe_load(default["yaml_text"])
    data["profiles"][0]["allowed"].append("pan_sear")
    body = {"expected_revision": 0, "yaml_text": yaml.safe_dump(data, allow_unicode=True), "reviewed": True}
    assert client.put("/v1/coach/method-policy", headers=env["cook"], json=body).status_code == 403
    assert (
        client.put("/v1/coach/method-policy", headers=headers, json=body | {"reviewed": False}).status_code
        == 422
    )
    assert client.put("/v1/coach/method-policy", headers=headers, json=body).status_code == 200
    assert client.put("/v1/coach/method-policy", headers=headers, json=body).status_code == 409
    assert client.get("/v1/coach/method-policy", headers=env["other"]).json()["revision"] == 0
    query = {"dish_title": "קורקבנים", "ingredients": []}
    public = client.post("/v1/coach/method-policy/options", json=query).json()
    private = client.post("/v1/coach/method-policy/my-options", headers=headers, json=query).json()
    assert "pan_sear" not in {item["id"] for item in public["allowed"]}
    assert "pan_sear" in {item["id"] for item in private["allowed"]}
    accepted = client.post(
        "/v1/coach/events",
        headers=headers,
        json={"action": "start_custom", "dish_title": "קורקבנים", "method": "pan_sear"},
    )
    assert accepted.status_code == 200
    rejected = client.post(
        "/v1/coach/preview",
        json={"command": {"action": "start_custom", "dish_title": "קורקבנים", "method": "pan_sear"}},
    )
    assert rejected.status_code == 422


def test_invalid_method_ids_and_empty_explanations_are_rejected(env):
    client, headers = env["client"], env["headers"]
    default = yaml.safe_load(client.get("/v1/coach/method-policy/template").json()["yaml_text"])
    for invalid in ("invented_method", ""):
        data = yaml.safe_load(yaml.safe_dump(default))
        if invalid:
            data["profiles"][0]["allowed"] = [invalid]
        else:
            data["profiles"][0]["reason"] = ""
        response = client.put(
            "/v1/coach/method-policy",
            headers=headers,
            json={
                "expected_revision": 0,
                "yaml_text": yaml.safe_dump(data),
                "reviewed": True,
            },
        )
        assert response.status_code == 422
