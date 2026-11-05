"""Finite, authored operation IDs and observations. No model or free-text parsing."""

from pydantic import Field

from app.cooking_intake import resolved_family
from app.knowledge import DomainError
from app.knowledge_graph import match_method
from app.schemas import StrictModel


class OperationEvent(StrictModel):
    operation_id: str = Field(max_length=80)
    outcome_id: str = Field(max_length=80)
    at: float
    reply: str = Field(max_length=2000)


def operation(key, label, group, instruction, checks, outcomes, *, heat=False):
    return {
        "id": key,
        "label": label,
        "group": group,
        "instruction": instruction,
        "checks": checks,
        "outcomes": [{"id": k, "label": v[0], "reply": v[1]} for k, v in outcomes.items()],
        "heat": heat,
    }


OPERATIONS = [
    operation(
        "organize",
        "סידור מרכיבים וכלים",
        "הכנה",
        "רכז את המרכיבים, בדוק כמויות והכן כלי מדידה, כלי עבודה וכלי הגשה נקי.",
        ["המרכיבים המרכזיים נמצאים", "הכלים מתאימים למתכון"],
        {
            "ready": ("הכול מוכן", "אפשר לבחור את פעולת ההכנה הבאה. השאר מזון מתכלה בקירור עד השימוש."),
            "missing": (
                "חסר לי מרכיב או כלי",
                "בדוק ברשימת המתכון מה חסר. ציין את שם המרכיב או הכלי ותפקידו; לפני החלפה צריך לברר אם הוא משפיע על מרקם, טעם או תהליך החימום.",
            ),
        },
    ),
    operation(
        "measure",
        "מדידת כמויות",
        "הכנה",
        "שקול או מדוד את הכמות לפי יחידות המתכון. הפרד בין משקל יבש למשקל מבושל.",
        ["היחידות תואמות למתכון", "ברור אם הכמות לפני או אחרי בישול"],
        {
            "measured": (
                "מדדתי לפי המתכון",
                "רשום את הכמות בשדה פרטי המנה כדי לשמור אותה. מדידה אינה משנה אוטומטית את שאר הכמויות.",
            ),
            "unknown": (
                "לא ברור כמה צריך",
                "חסרה רשימת כמויות למנה. הדבק מתכון עם מספר מנות וכמויות; בינתיים רכז את המרכיבים בלי להתחיל לערבב או לחמם.",
            ),
        },
    ),
    operation(
        "cut",
        "חיתוך",
        "הכנה",
        "השתמש בקרש יציב ובסכין מתאימה. חתוך לפי הגודל והצורה שנדרשים במתכון; חתיכות דומות מתבשלות בצורה אחידה יותר.",
        ["הקרש יציב", "גודל החתיכות דומה", "כלי מזון נא מופרדים מכלי הגשה"],
        {
            "even": (
                "החתיכות דומות בגודל",
                "הכן אותן לשלב הבא לפי המתכון. שמור בשר ודגים בקירור אם אינך מבשל מיד.",
            ),
            "uneven": (
                "החתיכות שונות מאוד",
                "אם אפשר, הקטן את הגדולות לגודל דומה. אחרת הפרד גדולות וקטנות כדי לבדוק אותן בנפרד במהלך הבישול.",
            ),
            "unknown": (
                "לא יודע איך לחתוך",
                "חסר גודל החיתוך הדרוש למנה. בדוק במתכון אם צריך קוביות, פרוסות או נתח שלם; הבא את השורה המתאימה לפני החיתוך.",
            ),
        },
    ),
    operation(
        "season",
        "תיבול וערבוב",
        "הכנה",
        "הוסף תיבול לפי כמויות המתכון וערבב לפיזור אחיד. אל תטעם תערובת שיש בה בשר, דגים, ביצים או קמח שטרם בושלו כנדרש.",
        ["התבלינים פוזרו", "הכמויות נמדדו ולא הוכפלו בטעות"],
        {
            "mixed": ("התיבול מעורבב", "המשך לפי המתכון. בדיקת טעם תיעשה רק בשלב שבו המזון מתאים לטעימה."),
            "unknown": (
                "חסרות לי כמויות תיבול",
                "צריך כמות חומר גלם וסגנון תיבול או מתכון. מלא את הכמות והתוצאה הרצויה; אל תוסיף מינון גדול כדי לפצות על חוסר ודאות.",
            ),
        },
    ),
    operation(
        "boil",
        "הגעה לרתיחה",
        "חימום",
        "עקוב אחר הנוזל בסיר בהתאם למתכון. כשיש רתיחה, בדוק אם השלב הבא דורש בעבוע עדין או המשך רתיחה.",
        ["יש נוזל בסיר", "ידוע אם דרושה רתיחה או בעבוע עדין"],
        {
            "boiling": (
                "הנוזל רותח",
                "לשלב של תבשיל בבעבוע עדין: הנמך את האש עד שבועות קטנות עולות ברוגע. לפסטה או לשלב שדורש רתיחה, פעל לפי המתכון. מה שמתרחש בנוזל אינו מוכיח שהמזון מוכן.",
            ),
            "not_boiling": (
                "הנוזל עדיין לא רותח",
                "המשך לעקוב לפי הוראות המתכון. בדוק שהכיריים פועלות ושיש נוזל; אל תשאיר את הסיר ללא השגחה.",
            ),
            "overflow": (
                "הנוזל גולש",
                "הפחת חום אם בטוח לעשות זאת והתרחק מהאדים. אל תיגע בסיר חם בידיים חשופות; המתן שהגלישה תירגע לפני המשך.",
            ),
        },
        heat=True,
    ),
    operation(
        "simmer",
        "בישול בבעבוע עדין",
        "חימום",
        "כוון לאש שמחזיקה בועות קטנות ועדינות. בדוק מדי פעם מפלס נוזל, תחתית ומרקם לפי המתכון.",
        ["אין רתיחה סוערת", "יש די נוזל", "אין חריכה בתחתית"],
        {
            "gentle": (
                "יש בעבוע עדין",
                "המשך לעקוב אחר הנוזל והרכות לפי המתכון. בחר בדיקת מרקם כשתרצה להעריך את הריכוך.",
            ),
            "vigorous": ("הרתיחה חזקה מדי", "הנמך את האש בהדרגה עד לבעבוע עדין. בדוק שוב לאחר שהנוזל נרגע."),
            "low_liquid": (
                "נשאר מעט נוזל",
                "הפחת חום ובדוק שאין חריכה. אם המתכון דורש בישול בנוזל, השלם בזהירות בנוזל המתאים לפי המתכון; אל תוסיף מים לשמן חם.",
            ),
        },
        heat=True,
    ),
    operation(
        "saute",
        "טיגון והשחמה במחבת",
        "חימום",
        "השתמש בכמות השמן ובחום שמתאימים למתכון. פזר בשכבה שאינה צפופה ועקוב אחר הצבע והריח.",
        ["אין עשן או חלקים שחורים", "המחבת אינה צפופה מדי"],
        {
            "browning": (
                "יש השחמה רצויה",
                "בדוק אם זה סוף שלב ההשחמה במתכון. צבע לבדו אינו מוכיח שהמרכז התבשל; המשך לבדיקת המוכנות המתאימה.",
            ),
            "pale": (
                "עדיין חיוור או מפריש נוזלים",
                "בדוק אם המחבת צפופה ואם המתכון דורש עבודה בכמה סבבים. אל תגביר חום אוטומטית בלי לבדוק שמן, כלי והוראות.",
            ),
            "burning": (
                "משחים מהר מדי או נחרך",
                "הפחת חום אם בטוח לעשות זאת. אל תערבב חלקים שחורים לתוך שאר המנה. אם יש אש, עצור את הליווי ופעל לפי הוראות החירום.",
            ),
        },
        heat=True,
    ),
    operation(
        "oven",
        "אפייה וצלייה בתנור",
        "חימום",
        "השתמש בחום, במיקום התבנית ובכיסוי שנדרשים במתכון. הכן כפפות וכלי הגשה נקי.",
        ["מצב התנור והטמפרטורה תואמים למתכון", "הכיסוי מתאים לכלי"],
        {
            "uneven": (
                "החלק העליון משחים לפני המרכז",
                "בדוק את מיקום התבנית ואת הוראות הכיסוי במתכון. השתמש בכפפות; השחמה חיצונית אינה בדיקת מוכנות במרכז.",
            ),
            "checking": (
                "הגעתי לשלב הבדיקה",
                "בחר בדיקת מרקם או מדידת טמפרטורה לפי סוג המנה. זמן שעבר בתנור אינו מחליף את הבדיקה.",
            ),
            "unknown": (
                "אין לי חום או זמן מתאימים",
                "חסרים נתוני אפייה למנה ולגודל הנתח. הבא מתכון שמציין חום, סוג תנור וסימני בדיקה; אל תבחר זמן אחיד לכל מנה.",
            ),
        },
        heat=True,
    ),
    operation(
        "texture",
        "בדיקת רכות ומרקם",
        "בדיקה",
        "בדוק חתיכה בכלי נקי לפי המרקם המבוקש: למשל התנגדות למזלג בירקות או בנתח לתבשיל. אל תשתמש בטעימה של מזון שטרם נבדקה מוכנותו.",
        ["נבדקה גם חתיכה גדולה", "המרקם מושווה לתוצאה הרצויה"],
        {
            "hard": (
                "עדיין קשה",
                "אם השלב במתכון הוא ריכוך בנוזל ויש מספיק נוזל, המשך בבעבוע עדין ובדוק שוב. בשיטה אחרת בדוק את הוראות המנה לפני הארכת הבישול.",
            ),
            "desired": (
                "המרקם כפי שרציתי",
                "בדיקת המרקם הושלמה לפי דיווחך. בדוק בנפרד את דרישות המוכנות של חומרי הגלם לפני הגשה; לא סימנתי את הפעולה כהושלמה.",
            ),
            "too_soft": (
                "רך מדי או מתפרק",
                "עצור את שלב הריכוך בהתאם למתכון והימנע מערבוב חזק. ריכוך שכבר קרה אינו מתהפך; אפשר לשקול הגשה במרקם אחר.",
            ),
        },
    ),
    operation(
        "temperature",
        "מדידת טמפרטורה",
        "בדיקה",
        "השתמש במדחום מזון ובדוק בחלקים העבים, בלי נגיעה בעצם. דווח את המספר בשדה מדידת הטמפרטורה.",
        ["המדידה בחלקים העבים", "המספר עצמו דווח"],
        {
            "measured": (
                "מדדתי — אזין את המספר",
                "הזן את המדידה בשדה הטמפרטורה. בחירה בכפתור הזה אינה שומרת מספר ואינה מאשרת מוכנות.",
            ),
            "no_thermometer": (
                "אין לי מדחום",
                "לא אוכל לאמת טמפרטורת ליבה מתוך מראה או זמן. החומר החסר הוא מדידה אמיתית במדחום מזון מתאים.",
            ),
        },
    ),
    operation(
        "sauce",
        "בדיקת סמיכות רוטב",
        "סיום",
        "בחן את סמיכות הרוטב בכלי נקי, בלי לטעום מזון שטרם בושל כנדרש.",
        ["הסמיכות מתאימה לצורת ההגשה", "אין חריכה בתחתית"],
        {
            "thick": (
                "סמיך מדי",
                "אם הרוטב מתאים לדילול, הוסף מעט מהנוזל המתאים למתכון בהדרגה וערבב. בדוק סמיכות אחרי כל תוספת.",
            ),
            "thin": (
                "דליל מדי",
                "אם המתכון מאפשר צמצום, בשל בבעבוע עדין ללא מכסה ועקוב שלא ייחרך. בדוק אם צריך להוציא קודם מרכיבים שעלולים להתבשל יתר על המידה.",
            ),
            "desired": (
                "הסמיכות מתאימה",
                "אין צורך להמשיך לצמצם רק מפני שהטיימר טרם הסתיים. בדוק את שאר דרישות המנה לפני ההגשה.",
            ),
        },
    ),
    operation(
        "serve",
        "הכנה להגשה",
        "סיום",
        "הכן כלי הגשה נקי. בדוק שהושלמו בדיקות המוכנות הדרושות למנה ודרישת מנוחה אם קיימת.",
        ["כלי ההגשה לא נגע במזון נא", "בדיקות המוכנות בוצעו"],
        {
            "ready": (
                "הכלים והבדיקות מוכנים",
                "הדיווח נשמר. בדוק את המדידות הרשומות ואת הוראות המתכון לפני הגשה; הבחירה אינה מסיימת אוטומטית את הבישול.",
            ),
            "missing": (
                "לא ברור אם הכול נבדק",
                "חזור לבדיקת המרקם ולבדיקת המוכנות של חומרי הגלם. אם חסרה מדידה או דרישת מנוחה, השלם אותה לפני הגשה.",
            ),
        },
    ),
]
BY_ID = {item["id"]: item for item in OPERATIONS}


def catalog(state):
    """Expose all supported operations, with explicit missing prerequisites."""
    family = resolved_family(state)
    selected_method = (state["context"]["graph"].get("method") or {}).get("id")
    if not selected_method and state["method"]:
        matched = match_method(state["method"])
        selected_method = matched["id"] if matched else None
    methods = {
        "boil": {"boil_simmer", "braise"},
        "simmer": {"boil_simmer", "braise"},
        "saute": {"pan_sear", "stir_fry"},
        "oven": {"oven_roast"},
    }
    result = []
    for item in OPERATIONS:
        reason = ""
        if item["heat"] and (not family or not state["method"]):
            reason = "בחר משפחת מנה ושיטת הכנה לפני הנחיות חימום."
        elif item["id"] in methods and selected_method not in methods[item["id"]]:
            reason = "הפעולה שייכת לשיטת הכנה אחרת. עדכן שיטה או בחר פעולה מתאימה."
        result.append({**item, "available": not reason, "reason": reason})
    return result


def select_operation(state, operation_id):
    item = next((item for item in catalog(state) if item["id"] == operation_id), None)
    if not item:
        raise DomainError("INVALID_OPERATION", "Choose an operation from the catalog", 422)
    if not item["available"]:
        raise DomainError("OPERATION_NEEDS_DETAILS", item["reason"], 422)
    state["selected_operation_id"] = operation_id
    return item["label"] + ": " + item["instruction"] + "\n\nבדוק: " + " · ".join(item["checks"])


def report_operation(state, operation_id, outcome_id, now):
    if operation_id != state.get("selected_operation_id"):
        raise DomainError("INVALID_OPERATION", "Select this operation before reporting", 422)
    # Recheck prerequisites on every command rather than trusting client metadata.
    select_operation(state, operation_id)
    item = BY_ID[operation_id]
    outcome = next((o for o in item["outcomes"] if o["id"] == outcome_id), None)
    if not outcome:
        raise DomainError("INVALID_OBSERVATION", "Choose an observation for the selected operation", 422)
    reply = outcome["reply"]
    if operation_id == "temperature" and state["context"]["minimum_temperature"] is not None:
        reply += f" הסף לחומר הגלם שזוהה הוא {state['context']['minimum_temperature']:g}°C."
    event = OperationEvent(operation_id=operation_id, outcome_id=outcome_id, at=now, reply=reply).model_dump()
    state["operation_events"] = (state.get("operation_events", []) + [event])[-50:]
    state["report_count"] += 1
    return reply


def attach_operations(state):
    state["operation_catalog"] = catalog(state)
