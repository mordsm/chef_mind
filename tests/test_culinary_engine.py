import shutil
from pathlib import Path

import pytest
import yaml
from app.method_policy import effective_policy, recommendations

from culinary_engine.src.config_manager import ConfigManager
from culinary_engine.src.sous_chef import SousChefEngine


@pytest.fixture
def config(tmp_path):
    source = Path(__file__).resolve().parents[1] / "culinary_engine" / "config"
    shutil.copytree(source, tmp_path / "config")
    return ConfigManager(tmp_path / "config")


def test_gizzard_block_and_persistent_add(config):
    chef = SousChefEngine(config)
    assert "oven_roast_dry" not in chef.get_allowed_methods("chicken_gizzard")
    result = chef.validate_method_choice("chicken_gizzard", "oven_roast_dry")
    assert result["allowed"] is False and result["error_code"] == "ERR_COLLAGEN_DRY"
    config.add_or_update_ingredient("beef_tongue", "לשון בקר", "dense_collagen_lean")
    assert chef.get_allowed_methods("beef_tongue") == chef.get_allowed_methods("chicken_gizzard")
    assert ConfigManager(config.config_dir).registry_data["ingredients"]["beef_tongue"]["name"] == "לשון בקר"


def test_invalid_update_preserves_memory_and_source(config):
    before = config.get_raw_rules_yaml()
    invalid = yaml.safe_load(before)
    invalid["archetypes"].pop("dense_collagen_lean")
    with pytest.raises(ValueError):
        config.save_raw_rules_yaml(yaml.safe_dump(invalid))
    assert config.get_raw_rules_yaml() == before
    assert "dense_collagen_lean" in config.rules_data["archetypes"]
    registry = config.get_raw_registry_yaml()
    with pytest.raises(ValueError):
        config.add_or_update_ingredient("test", "test", "missing")
    assert config.get_raw_registry_yaml() == registry


@pytest.mark.parametrize(
    "raw",
    [
        "ingredients: {}\ningredients: {}",
        "ingredients: &a {test: *a}",
        "ingredients: {test: {name: x, archetype: missing}}",
    ],
)
def test_invalid_registry(config, raw):
    with pytest.raises(ValueError):
        config.save_raw_registry_yaml(raw)


def test_reload_and_raw_preservation(config):
    chef = SousChefEngine(config)
    raw = config.get_raw_rules_yaml()
    changed = yaml.safe_load(raw)
    family = changed["archetypes"]["dense_collagen_lean"]
    family["allowed_methods"].remove("sous_vide")
    text = "# preserved comment\n" + yaml.safe_dump(changed, allow_unicode=True, sort_keys=False)
    config.save_raw_rules_yaml(text)
    assert config.get_raw_rules_yaml() == text
    assert "sous_vide" not in chef.get_allowed_methods("chicken_gizzard")
    config.reload()
    assert "sous_vide" not in chef.get_allowed_methods("chicken_gizzard")
    assert chef.validate_method_choice("chicken_gizzard", "sous_vide")["allowed"] is False
    assert chef.validate_method_choice("missing", "steam")["allowed"] is False


def test_runtime_uses_registry(monkeypatch, config):
    import app.culinary_engine_api as adapter

    monkeypatch.setattr(adapter, "CONFIG_DIR", config.config_dir)
    config.add_or_update_ingredient("beef_tongue", "לשון בקר", "dense_collagen_lean")
    options = recommendations("לשון בקר", [], effective_policy()["policy"])
    assert options["profile_id"] == "engine_beef_tongue"
    assert {x["id"] for x in options["allowed"]} == {"braise", "boil_simmer"}


def test_source_api_permissions_conflict_and_live_update(env, monkeypatch, config):
    import app.culinary_engine_api as adapter

    monkeypatch.setattr(adapter, "CONFIG_DIR", config.config_dir)
    client = env["client"]
    state = client.get("/v1/culinary/engine").json()
    body = {
        "expected_revision": state["revision"],
        "reviewed": True,
        "name": "לשון בקר",
        "archetype": "dense_collagen_lean",
    }
    url = "/v1/culinary/engine/ingredients/beef_tongue"
    assert client.put(url, json=body).status_code == 401
    assert client.put(url, json=body, headers=env["cook"]).status_code == 403
    saved = client.put(url, json=body, headers=env["headers"])
    assert saved.status_code == 200, saved.text
    assert client.put(url, json=body, headers=env["headers"]).status_code == 409
    assert "beef_tongue" in config.get_raw_registry_yaml()
    result = client.post(
        "/v1/culinary/engine/validate", json={"ingredient_key": "beef_tongue", "method_key": "oven_roast_dry"}
    ).json()
    assert result["allowed"] is False and result["error_code"] == "ERR_COLLAGEN_DRY"
    body = {"expected_revision": saved.json()["revision"], "reviewed": True, "yaml_text": "archetypes: {}"}
    assert (
        client.put("/v1/culinary/engine/sources/rules", json=body, headers=env["headers"]).status_code == 422
    )
    assert client.get("/v1/culinary/engine/ingredients/unknown/methods").status_code == 404
