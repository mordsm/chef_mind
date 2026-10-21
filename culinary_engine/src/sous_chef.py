"""Deterministic compatibility decisions from the current configuration."""


class SousChefEngine:
    def __init__(self, config_manager):
        self.cfg = config_manager

    def get_allowed_methods(self, ingredient_key):
        ingredient = self.cfg.registry_data["ingredients"].get(ingredient_key)
        if ingredient is None:
            raise KeyError(f"Unknown ingredient: {ingredient_key}")
        family = self.cfg.rules_data["archetypes"].get(ingredient["archetype"])
        if family is None:
            raise ValueError("Unknown archetype")
        return list(family["allowed_methods"])

    def validate_method_choice(self, ingredient_key, method_key):
        ingredient = self.cfg.registry_data["ingredients"].get(ingredient_key)
        if ingredient is None:
            return {"allowed": False, "error_code": "ERR_UNKNOWN_INGREDIENT", "error": "חומר גלם לא מוכר"}
        allowed = self.get_allowed_methods(ingredient_key)
        result = {"ingredient": ingredient["name"], "method": method_key}
        if method_key in allowed:
            return result | {"allowed": True, "message": "השיטה מתאימה לפי קובץ החוקים."}
        family = self.cfg.rules_data["archetypes"][ingredient["archetype"]]
        reason = self.cfg.rules_data["failure_reasons"].get(family["blocked_methods"].get(method_key), {})
        return result | {
            "allowed": False,
            "error_code": reason.get("code", "ERR_METHOD_UNDEFINED"),
            "reason": reason.get("message", "לא הוגדר חוק המתיר שיטה זו לחומר הגלם."),
            "recommended_alternatives": allowed,
        }
