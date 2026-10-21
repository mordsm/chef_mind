"""Small, explicit policy baseline; unknown facts never become safety certification."""

import re

from app.schemas import ChefRequest

VERSION = "baseline-0.1"
MEAT = {"meat", "chicken", "turkey", "beef", "בשר", "עוף", "הודו", "בקר"}
DAIRY = {"milk", "butter", "cream", "cheese", "חלב", "חמאה", "שמנת", "גבינה"}
HAZARDS = ("oil fire", "pan on fire", "שמן עולה באש", "המחבת בוערת")
FORBIDDEN = (
    "i can see",
    "i measured",
    "i tasted",
    "אני רואה",
    "מדדתי",
    "טעמתי",
    "ignore allergies",
    "ignore all previous instructions",
    "התעלם מאלרגיות",
    "אין צורך במדחום",
    "safe by color alone",
    "בטוח לפי הצבע בלבד",
)
ALLERGEN_GROUPS = (
    {"milk", "dairy", "butter", "cream", "cheese", "חלב", "חמאה", "שמנת", "גבינה"},
    {"peanut", "peanuts", "בוטנים", "בוטן"},
    {"sesame", "tahini", "שומשום", "טחינה"},
)


def allergens(values):
    expanded = {value.lower() for value in values}
    for group in ALLERGEN_GROUPS:
        if expanded & group:
            expanded |= group
    return expanded


def words(text):
    return set(re.findall(r"[^\W_]+", text.lower()))


def forbidden(text):
    text = text.lower()
    return any(phrase in text for phrase in FORBIDDEN)


def assess(request: ChefRequest, proposed=""):
    context = " ".join([request.message, *request.state.reports, proposed]).lower()
    if any(hazard in context for hazard in HAZARDS):
        return "blocked", "SAFETY_HAZARD", "יש לטפל בסיכון לפני המשך הבישול; אין לבצע את הפעולה המוצעת."
    if forbidden(proposed):
        return "blocked", "UNSAFE_SOURCE_ACTION", "הפעולה מתנגשת עם כללי הבטיחות ואינה מאושרת."
    classes = {item.food_class for item in request.inventory if item.verified and item.quantity != 0}
    action_words = words(proposed)
    if action_words & MEAT:
        classes.add("meat")
    if action_words & DAIRY:
        classes.add("dairy")
    if request.profile.forbid_meat_dairy and {"meat", "dairy"} <= classes:
        return (
            "blocked",
            "MEAT_DAIRY_CONFLICT",
            "הרכיבים הבשריים והחלביים אינם מתאימים יחד לפרופיל הכשרות שלך.",
        )
    allergies = allergens(request.profile.allergies)
    if allergies:
        for item in request.inventory:
            if (allergens(item.allergens) | allergens(words(item.name))) & allergies:
                return (
                    "blocked",
                    "ALLERGEN_CONFLICT",
                    "דווח על אלרגן שאינו מתאים לפרופיל שלך; אין להשתמש ברכיב הזה.",
                )
        if any(not item.label_verified for item in request.inventory):
            return (
                "clarify",
                "ALLERGEN_LABEL_UNVERIFIED",
                "יש לבדוק תוויות וחשש למגע צולב לפני בחירת תחליף או רכיב.",
            )
        if allergies & action_words:
            return "blocked", "ALLERGEN_CONFLICT", "הפעולה כוללת אלרגן שאסרת."
    if request.profile.forbid_meat_dairy and any(
        item.verified and item.food_class == "unknown" for item in request.inventory
    ):
        return "clarify", "KASHRUT_UNVERIFIED", "מה הסיווג וההכשר הרלוונטיים של המוצרים הלא מאומתים?"
    if request.state.safety_question or (
        words(context) & MEAT
        and any(term in context for term in ("safe", "done", "בטוח", "מוכן", "טמפרטורה"))
    ):
        return (
            "clarify",
            "SAFETY_FACTS_REQUIRED",
            "אין לאשר מוכנות לפי זמן או צבע בלבד. נדרשים נתוני מדידה וכלל בטיחות מתאים ממקור מוסמך.",
        )
    return None


def missing_ingredients(request, required):
    inventory = {item.name.lower(): item for item in request.inventory}
    return [
        name
        for name in required
        if name.lower() not in inventory
        or not inventory[name.lower()].verified
        or inventory[name.lower()].quantity is None
        or inventory[name.lower()].quantity <= 0
    ]
