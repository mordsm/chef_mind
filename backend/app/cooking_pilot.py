"""Bounded cold-salad pilot and explicit reminder requests; no inferred completion."""

import re

from app.ingredient_safety import contains, ingredient_groups, normalize

PRODUCE_SOURCE = "https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-produce-safely"
PILOT_SOURCE = "CHEF_AUTHORED:salad_pilot_v1"
KNOWN = (
    "מלפפון",
    "מלפפונים",
    "עגבנייה",
    "עגבניה",
    "עגבניות",
    "חסה",
    "גזר",
    "פלפל",
    "בצל",
    "שמן זית",
    "לימון",
    "מלח",
    "חומץ",
)


def timer_request(text):
    if re.search(r"אל\s+תפעיל|לא\s+להפעיל|do not|don't|cancel|בטל", text, re.IGNORECASE):
        return None
    if not re.search(r"הפעל.*תזכורת|תזכיר לי|set.*timer|remind me", text, re.IGNORECASE):
        return None
    amounts = {"שתי": 2, "שניים": 2, "שתיים": 2, "שלוש": 3, "חמש": 5}
    match = re.search(
        r"(?<![\d.,\-])(\d+|שתי|שניים|שתיים|שלוש|חמש)\s*(שניות|דקות|seconds?|minutes?)(?!\w)",
        text,
        re.IGNORECASE,
    )
    if not match:
        return None
    number = int(match[1]) if match[1].isdigit() else amounts[match[1]]
    seconds = number * (60 if match[2].lower() in ("דקות", "minute", "minutes") else 1)
    return seconds if 1 <= seconds <= 14400 else None


def is_salad_pilot(state):
    return any(step.get("source") == PILOT_SOURCE for step in state.get("custom_steps", []))


def ensure_salad_plan(state):
    if (
        state.get("status") != "active"
        or state.get("custom_steps")
        or state.get("safety_hold")
        or not contains(state["dish_title"], "סלט")
    ):
        return False
    facts = state.get("intake_facts") or {}
    names = state.get("ingredients", [])
    if not facts.get("quantity") or not facts.get("equipment") or len(names) < 2 or state.get("method"):
        return False
    # No fish, meat, eggs, dairy, raw legumes or unknown mixtures in this pilot.
    if any(
        ingredient_groups(name) or normalize(name) not in {normalize(known) for known in KNOWN}
        for name in names
    ):
        return False
    if not any(contains(name, veg) for name in names for veg in KNOWN[:9]):
        return False
    from app.consultant import user_step

    definitions = [
        (
            "שטיפת הירקות",
            f"השתמש בכמות הירקות שבחרת: {facts['quantity']}. שטוף ידיים והכן קרש וסכין נקיים, שלא נגעו בבשר או בדג נא. שטוף את הירקות במים זורמים; אל תשתמש בסבון על הירקות. דווח כשהירקות והכלים מוכנים.",
            "הירקות נשטפו והכלים נקיים",
        ),
        (
            "חיתוך הירקות",
            "חתוך את הירקות לחתיכות בגודל דומה והעבר לקערה נקייה. אם משתמשים בחסה, יבש את העלים כדי שהרוטב לא יידלל. דווח כשהחיתוך הושלם.",
            "הירקות חתוכים ומוכנים בקערה",
        ),
        (
            "ערבוב הרוטב",
            "הכן קערית נפרדת. נסה כמה טיפות לימון או חומץ ומעט שמן זית, רק מתוך הרכיבים שיש לך. ערבב וטעם על חתיכת ירק. הוסף קמצוץ מלח אם חסר, ונסה שוב. אל תשפוך עדיין את כל הרוטב על הסלט.",
            "הרוטב נטעם על חתיכת ירק והטעם מתאים לך",
        ),
        (
            "תיבול והגשה",
            "הוסף מעט מהרוטב לירקות, ערבב וטעם. הוסף עוד רק אם צריך. הגש בכלים נקיים. אם שומרים להמשך, הכנס את הירקות החתוכים לכלי סגור במקרר קר, מתחת ל־4°C; עדיף לשמור את הרוטב בנפרד. דווח כשההגשה או האחסון הושלמו.",
            "הסלט הוגש או נשמר בקירור",
        ),
    ]
    for title, instruction, check in definitions:
        step = user_step(title, instruction, state["context"])
        step.update(source=PILOT_SOURCE, successCriteria=[check], chefQuestions=[check + "?"])
        state["custom_steps"].append(step)
    state["current_step"] = 0
    state["completed_step_ids"] = []
    state["guidance_links"] = [{"title": "FDA — שטיפה ואחסון של ירקות", "url": PRODUCE_SOURCE}]
    return True


def remember_request(state, text):
    memory = state.setdefault("cooking_memory", {})
    if "אין לי" not in text and any(
        term in text
        for term in ("נשרף", "חמוץ מדי", "מלוח מדי", "לא תפח", "עדיין קשה", "יבש מדי", "מוציא מים")
    ):
        memory["reported_problem"] = text[:1000]
    if "אין לי" in text:
        memory["missing_ingredient_report"] = text[:1000]


def salad_reply(state, text):
    if not is_salad_pilot(state):
        return None
    steps = state["custom_steps"]
    current = steps[state["current_step"]]
    if "חזור לבישול" in text or "מה דיווחתי" in text:
        memory = state.get("cooking_memory", {})
        return (
            "אתה מכין "
            + state["dish_title"]
            + ".\n"
            + "\n".join(
                label + memory[key]
                for key, label in (
                    ("reported_problem", "התקלה שדיווחת: "),
                    ("missing_ingredient_report", "החוסר שדיווחת: "),
                )
                if key in memory
            )
            + "\nהפעולה הבאה: "
            + current["instruction"]
        )
    if "אין לי לימון" in text:
        return "אפשר לנסות כמה טיפות חומץ במקום לימון בכף רוטב נפרדת, ואז לטעום על ירק. הוסף בהדרגה; הטעם יהיה שונה. אל תחליף את כל הכמות בבת אחת."
    if "חמוץ מדי" in text:
        return "אל תוסיף עוד לימון או חומץ. קח כף מהרוטב לקערית נפרדת, הוסף מעט שמן ונסה על חתיכת ירק. האם הטעם השתפר? אם הרוטב כבר עורבב בכל הסלט, דווח לפני שמשנים את הכמות כולה."
    if "מוציא מים" in text:
        return "אל תוסיף כרגע עוד רוטב. אם הצטבר נוזל בתחתית הקערה, סנן אותו בעדינות וטעם חתיכת ירק לפני תיבול נוסף."
    if "שליקה" in text:
        return "שליקה היא בישול בנוזל חם שאינו רותח בחוזקה. בסלט הזה אין צורך לבשל. אנחנו נשארים במנה ובשלב שבחרת."
    if any(word in text for word in ("נפרדים", "השמן", "למה", "מדע")):
        return "שמן ומיץ לימון נפרדים כשמניחים אותם לעמוד. ערבוב מפזר את השמן בטיפות קטנות לזמן מה; ערבב שוב לפני ההוספה לסלט."
    if any(word in text for word in ("לשמור", "אחסון", "הגשה", "מוכנה", "מה למדתי")):
        return steps[-1]["instruction"] + " אין בסלט הזה שלב חימום. למדנו לטעום מעט לפני שמתבלים את כל הכמות."
    return current["instruction"] + " בדוק: " + current["successCriteria"][0] + "."
