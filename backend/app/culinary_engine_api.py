"""Shared source editor and adapter for the standalone culinary engine."""

import hashlib
from pathlib import Path
from threading import RLock

from fastapi import Depends
from pydantic import Field

from app.knowledge import DomainError
from app.schemas import StrictModel
from culinary_engine.src.config_manager import ConfigManager
from culinary_engine.src.sous_chef import SousChefEngine

CONFIG_DIR = Path(__file__).resolve().parents[2] / "culinary_engine" / "config"
LOCK = RLock()
METHOD_MAP = {"oven_roast_dry": "oven_roast", "braise_slow_cook": "braise"}


def configuration():
    return ConfigManager(CONFIG_DIR)


def snapshot(cfg):
    rules, registry = cfg.get_raw_rules_yaml(), cfg.get_raw_registry_yaml()
    return {
        "rules_yaml": rules,
        "registry_yaml": registry,
        "revision": hashlib.sha256((rules + "\0" + registry).encode()).hexdigest(),
        "source_paths": {
            "rules": str(cfg.rules_path.relative_to(CONFIG_DIR.parent.parent)),
            "registry": str(cfg.registry_path.relative_to(CONFIG_DIR.parent.parent)),
        },
        "ingredients": cfg.registry_data["ingredients"],
        "archetypes": cfg.rules_data["archetypes"],
    }


def profiles(labels):
    cfg = configuration()
    chef = SousChefEngine(cfg)
    result = []
    for key, ingredient in cfg.registry_data["ingredients"].items():
        terms = [ingredient["name"], key.replace("_", " ")]
        if key == "chicken_gizzard":
            terms += ["קורקבנים", "קוקבנים", "gizzards"]
        if key == "beef_shank":
            terms += ["שוק בקר", "אוסובוקו"]
        if key == "nile_perch":
            terms += ["nile perch", "lates niloticus"]
        allowed = [METHOD_MAP.get(m, m) for m in chef.get_allowed_methods(key)]
        # Compatibility alone cannot approve a process requiring validation.
        allowed = [m for m in allowed if m in labels and m not in ("sous_vide", "raw_cure")]
        blocked = {}
        for method in labels:
            engine_method = next((k for k, v in METHOD_MAP.items() if v == method), method)
            decision = chef.validate_method_choice(key, engine_method)
            reason = decision.get("reason", "שיטה זו דורשת תהליך מאומת נוסף לפני הפעלה.")
            blocked[method] = reason
        result.append(
            {
                "id": "engine_" + key,
                "title": ingredient["name"],
                "ingredient_ids": [],
                "title_terms": terms,
                "family": "",
                "allowed": allowed,
                "reason": "השיטות נקבעו לפי משפחת חומר הגלם בקובץ חוקי המנוע.",
                "blocked_reasons": blocked,
            }
        )
    return result


class SourceUpdate(StrictModel):
    expected_revision: str = Field(min_length=64, max_length=64)
    yaml_text: str = Field(max_length=256000)
    reviewed: bool = False


class IngredientUpdate(StrictModel):
    expected_revision: str = Field(min_length=64, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    archetype: str = Field(min_length=1, max_length=80)
    reviewed: bool = False


class MethodChoice(StrictModel):
    ingredient_key: str = Field(max_length=80)
    method_key: str = Field(max_length=80)


def install_engine_routes(app, reviewer):
    reviewer_dependency = Depends(reviewer)

    @app.get("/v1/culinary/engine")
    def read():
        with LOCK:
            return snapshot(configuration())

    @app.post("/v1/culinary/engine/validate")
    def choice(body: MethodChoice):
        return SousChefEngine(configuration()).validate_method_choice(body.ingredient_key, body.method_key)

    @app.get("/v1/culinary/engine/ingredients/{key}/methods")
    def methods(key: str):
        try:
            return {
                "allowed_methods": SousChefEngine(configuration()).get_allowed_methods(key),
                "scope": "compatibility; validated process requirements apply separately",
            }
        except KeyError as exc:
            raise DomainError("UNKNOWN_INGREDIENT", "חומר גלם לא מוכר", 404) from exc

    def update(body, mutate):
        with LOCK:
            cfg = configuration()
            if not body.reviewed:
                raise DomainError("REVIEW_REQUIRED", "יש לאשר את השינוי המשותף לכל המשתמשים", 422)
            if snapshot(cfg)["revision"] != body.expected_revision:
                raise DomainError("SOURCE_CONFLICT", "המקור השתנה; יש לטעון מחדש", 409)
            try:
                mutate(cfg)
            except ValueError as exc:
                raise DomainError("INVALID_ENGINE_SOURCE", str(exc), 422) from exc
            return snapshot(cfg)

    @app.put("/v1/culinary/engine/sources/{source}")
    def save(source: str, body: SourceUpdate, owner=reviewer_dependency):
        if source not in ("rules", "registry"):
            raise DomainError("UNKNOWN_SOURCE", "מקור לא מוכר", 404)
        return update(
            body,
            lambda cfg: (cfg.save_raw_rules_yaml if source == "rules" else cfg.save_raw_registry_yaml)(
                body.yaml_text
            ),
        )

    @app.put("/v1/culinary/engine/ingredients/{key}")
    def ingredient(key: str, body: IngredientUpdate, owner=reviewer_dependency):
        return update(body, lambda cfg: cfg.add_or_update_ingredient(key, body.name, body.archetype))
