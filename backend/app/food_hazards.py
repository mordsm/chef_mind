"""Ingredient-state warnings checked before ordinary technique guidance."""
from app.ingredient_safety import contains

BEAN_SOURCE = "https://www.fda.gov/food/chemical-contaminants-pesticides/natural-toxins-food"


def red_bean_warning(names, message=""):
    text = " ".join([*names, message])
    if not any(contains(text, value) for value in ("שעועית אדומה", "red kidney beans", "red kidney bean")):
        return None
    dry = any(contains(text, value) for value in ("יבשה", "יבשים", "יבשות", "dry", "dried", "השריתי", "להשרות"))
    canned = any(contains(text, value) for value in ("משומרת", "משימורים", "canned", "tinned"))
    cooked = any(contains(text, value) for value in ("מבושלת מראש", "previously cooked"))
    if (canned or cooked) and not dry:
        return None
    return {
        "text": (
            "עצור לפני בישול שעועית אדומה יבשה בסיר איטי על חום נמוך. השריה לבדה אינה מספיקה כדי להפוך אותה לבטוחה. "
            "לפי מדריך FDA, לשעועית יבשה יש להשרות לפחות 5 שעות, לשפוך את מי ההשריה, "
            "ולהרתיח במים טריים לפחות 30 דקות. רכות בלבד אינה בדיקת בטיחות. "
            "אם אינך בטוח כיצד הוכנה, בחר שעועית משומרת מוכנה לאכילה ופעל לפי הוראות האריזה."
        ),
        "question": "האם השעועית יבשה, משומרת או מבושלת מראש?" if not dry else "האם הושלמו ההשריה וההרתחה הנדרשות לפני השימוש בסיר האיטי?",
        "source": BEAN_SOURCE,
        "source_id": "FDA-NATURAL-TOXINS-BEANS",
    }
