"""Twenty source-grounded cooking scenarios. Not professional kitchen validation."""

from app.chef import respond
from app.schemas import ChefRequest

SCENARIOS = [
    ("starch-ready", "starch", "starch-slurry", "מסמיכים רוטב בקורנפלור", True, "action"),
    ("starch-condition", "starch", "starch-slurry", "", True, "clarify"),
    ("starch-missing", "starch", "starch-slurry", "מסמיכים רוטב בקורנפלור", False, "clarify"),
    ("starch-quiet", "starch", "starch-slurry", "מסמיכים רוטב בקורנפלור", True, "action"),
    ("custard-ready", "custard", "custard-curdling", "קרם הביצים מתחיל להתגבן", True, "action"),
    ("custard-condition", "custard", "custard-curdling", "", True, "clarify"),
    ("custard-quiet", "custard", "custard-curdling", "קרם הביצים מתחיל להתגבן", True, "action"),
    ("custard-report", "custard", "custard-curdling", "קרם הביצים מתחיל להתגבן", True, "action"),
    ("sugar-ready", "sugar", "sugar-crystals", "מכינים סירופ סוכר חלק ולא ממתק גבישי", True, "action"),
    ("sugar-condition", "sugar", "sugar-crystals", "", True, "clarify"),
    ("sugar-quiet", "sugar", "sugar-crystals", "מכינים סירופ סוכר חלק ולא ממתק גבישי", True, "action"),
    ("sugar-fire", "oil fire", None, "", True, "blocked"),
    (
        "cut-ready",
        "collagen",
        "collagen-moist-heat",
        "הנתח זוהה כעשיר ברקמת חיבור ומתאים לבישול לח",
        True,
        "action",
    ),
    ("cut-condition", "collagen", "collagen-moist-heat", "", True, "clarify"),
    (
        "cut-quiet",
        "collagen",
        "collagen-moist-heat",
        "הנתח זוהה כעשיר ברקמת חיבור ומתאים לבישול לח",
        True,
        "action",
    ),
    ("cut-safety", "is chicken safe by color", None, "", True, "clarify"),
    (
        "probe-ready",
        "thermometer",
        "thermometer-placement",
        "יש מדחום מזון מתאים ויודעים מהו סוג הבשר",
        True,
        "action",
    ),
    ("probe-condition", "thermometer", "thermometer-placement", "", True, "clarify"),
    (
        "probe-quiet",
        "thermometer",
        "thermometer-placement",
        "יש מדחום מזון מתאים ויודעים מהו סוג הבשר",
        True,
        "action",
    ),
    ("unsupported", "zzunsupportedrecipezz", None, "", True, "insufficient_evidence"),
]


def run_culinary_suite(session, owner):
    results = []
    for name, query, knowledge_id, condition, available, expected in SCENARIOS:
        body = ChefRequest(
            cooking_id=name,
            message=query,
            state={"current_goal": query},
            confirmed_conditions=[condition] if condition else [],
            profile={"explanation": "quiet" if "quiet" in name else "short"},
            inventory=[{"name": "קורנפלור", "quantity": 1, "verified": True, "food_class": "pareve"}]
            if available
            else [],
        )
        decision = respond(session, owner, body)
        actual_ids = [citation.knowledge_id for citation in decision.citations]
        passed = decision.decision_type == expected
        if expected == "action":
            passed = passed and knowledge_id in actual_ids and bool(decision.instruction)
            passed = passed and decision.estimated_check_time is None
            passed = passed and all(c.attribution and c.license_reference for c in decision.citations)
        results.append(
            {
                "id": name,
                "passed": passed,
                "expected": expected,
                "actual": decision.decision_type,
                "citation_ids": actual_ids,
            }
        )
    return {
        "suite": "culinary-sources-0.1",
        "passed": all(r["passed"] for r in results),
        "cases": results,
        "limitations": "Requires five reviewed corpus drafts active for this owner; offline behavioral checks, not kitchen trials or model quality certification.",
    }
