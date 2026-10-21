import yaml
from app.culinary_sources import FILES
from app.db import AuditEvent, CulinarySourceRevision
from sqlalchemy import func, select

BASE = "/v1/culinary/sources"


def read(env, key="graph", headers="headers", suffix=""):
    return env["client"].get(f"{BASE}/{key}{suffix}", headers=env[headers])


def add(env, key="graph", expected=0, entry_id="new_vegetable"):
    return env["client"].post(
        f"{BASE}/{key}/entries",
        headers=env["headers"],
        json={
            "expected_revision": expected,
            "section": "base_ingredients",
            "entry_id": entry_id,
            "yaml_text": 'name: "ירק חדש"\ncategory: vegetables\nbase_rules: []\n',
        },
    )


def test_originals_load_and_access_is_scoped(env):
    assert env["client"].get(BASE).status_code == 401
    result = env["client"].get(BASE, headers=env["headers"])
    assert result.status_code == 200
    assert len(result.json()["items"]) == 2
    for key in FILES:
        source = read(env, key).json()
        assert source["revision"] == 0
        assert source["used_by_coach"] is False
        assert source["yaml_text"] == FILES[key].read_text(encoding="utf-8-sig")
    assert read(env, "invalid").status_code == 422
    assert read(env, suffix="?revision=-1").status_code == 422
    assert read(env, suffix="?revision=99").status_code == 404


def test_original_templates_are_public_but_private_edits_are_not(env):
    for key in FILES:
        response = env["client"].get(f"/v1/culinary/templates/{key}")
        assert response.status_code == 200
        assert response.json()["yaml_text"] == FILES[key].read_text(encoding="utf-8-sig")
    assert add(env).status_code == 201
    original = env["client"].get("/v1/culinary/templates/graph").json()
    assert original["revision"] == 0
    assert "new_vegetable" not in original["yaml_text"]


def test_add_persists_history_and_isolates_owners(env):
    originals = {key: path.read_bytes() for key, path in FILES.items()}
    for key in FILES:
        result = add(env, key)
        assert result.status_code == 201, result.text
        source = result.json()
        assert source["revision"] == 1
        assert yaml.safe_load(source["yaml_text"])["base_ingredients"]["new_vegetable"]["name"] == "ירק חדש"
        assert read(env, key).json()["yaml_text"] == source["yaml_text"]
        assert read(env, key, "other").json()["revision"] == 0
        assert "new_vegetable" not in read(env, key, suffix="?revision=0").json()["yaml_text"]
        assert read(env, key, suffix="?revision=1").json()["yaml_text"] == source["yaml_text"]
    assert all(path.read_bytes() == originals[key] for key, path in FILES.items())
    with env["app"].state.engine.connect() as connection:
        assert connection.scalar(select(func.count()).select_from(CulinarySourceRevision)) == 2
        assert connection.scalar(select(func.count()).select_from(AuditEvent)) == 2


def test_permissions_conflict_and_revert(env):
    original = read(env).json()["yaml_text"]
    assert (
        env["client"]
        .put(
            f"{BASE}/graph",
            headers=env["cook"],
            json={
                "expected_revision": 0,
                "yaml_text": original,
            },
        )
        .status_code
        == 403
    )
    assert add(env).status_code == 201
    stale = env["client"].put(
        f"{BASE}/graph",
        headers=env["headers"],
        json={
            "expected_revision": 0,
            "yaml_text": original,
        },
    )
    assert stale.status_code == 409
    assert add(env, expected=1).status_code == 409
    restored = env["client"].put(
        f"{BASE}/graph",
        headers=env["headers"],
        json={
            "expected_revision": 1,
            "yaml_text": original,
        },
    )
    assert restored.status_code == 200
    assert restored.json()["revision"] == 2
    assert read(env, suffix="?revision=1").json()["revision"] == 1


def test_invalid_yaml_and_references_do_not_save(env):
    original = read(env).json()["yaml_text"]
    invalid = ["[", "a: 1\na: 2", "!!python/object:thing {}", "a: &a [*a]", "{}"]
    data = yaml.safe_load(original)
    data["recipe_paths"][0]["ingredient_ref"] = "missing"
    invalid.append(yaml.safe_dump(data))
    for text in invalid:
        result = env["client"].put(
            f"{BASE}/graph",
            headers=env["headers"],
            json={
                "expected_revision": 0,
                "yaml_text": text,
            },
        )
        assert result.status_code == 422, result.text
    assert read(env).json()["revision"] == 0


def test_add_recipe_and_reject_missing_reference(env):
    path = {
        "title": "New path",
        "ingredient_ref": "chicken_breast",
        "method_ref": "pan_sear",
        "specific_steps": [{"action": "Draft action"}],
    }

    def post(value):
        return env["client"].post(
            f"{BASE}/graph/entries",
            headers=env["headers"],
            json={
                "expected_revision": 0,
                "section": "recipe_paths",
                "yaml_text": yaml.safe_dump(value),
            },
        )

    path["method_ref"] = "missing"
    assert post(path).status_code == 422
    path["method_ref"] = "pan_sear"
    assert post(path).status_code == 201
