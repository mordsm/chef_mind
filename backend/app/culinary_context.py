"""Reusable dish-family knowledge. Suggestions are not complete recipes or safety observations."""

import re

from pydantic import Field

from app.knowledge_graph import GraphContext, graph_context
from app.schemas import StrictModel

TECHNIQUE = "https://www.ciachef.edu/blog/3-types-cooking-methods-foods-love/"
SAFETY = "https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures"


class ContextTip(StrictModel):
    title: str = Field(max_length=160)
    text: str = Field(max_length=1000)
    source: str = Field(max_length=1000)
    origin: str = Field(default="EDITORIAL", max_length=60)
    source_ids: list[str] = Field(default_factory=list, max_length=16)


class DishContext(StrictModel):
    family: str = Field(max_length=40)
    label: str = Field(max_length=120)
    method: str = Field(max_length=160)
    identified: bool
    tips: list[ContextTip] = Field(max_length=8)
    questions: list[str] = Field(max_length=8)
    suggestions: list[str] = Field(max_length=12)
    minimum_temperature: float | None = None
    sources: list[str] = Field(max_length=8)
    graph: GraphContext | None = None
    minimum_rest_seconds: int = 0


FAMILIES = [
    (
        "poultry",
        "עוף והודו",
        {"הודו", "עוף", "עופות", "turkey", "chicken", "poultry"},
        "נתחי עוף והודו שונים בגודל ובמבנה. אפשר לבחור צלייה או בישול בנוזל לפי התוצאה הרצויה; אין זמן אחד שמתאים לכל נתח.",
        ["איזו שיטת הכנה אתה מתכנן — תנור, סיר או מחבת?", "מה משקל הנתחים והאם הם מופשרים?"],
        ["הכנה ותיבול", "הכנה בשיטה שבחרת", "בדיקת טמפרטורה"],
        74,
    ),
    (
        "pasta",
        "פסטה ואטריות",
        {"פסטה", "ספגטי", "מקרוני", "אטריות", "pasta", "spaghetti", "noodles"},
        "אפשר להכין את הפסטה והרוטב בנפרד ולחבר בסוף. בדוק את הוראות האריזה; מרקם הרוטב והפסטה חשוב יותר מטיימר אחיד.",
        ["איזה רוטב אתה מתכנן — מבושל או מהיר?", "מה סוג הפסטה?"],
        ["הכנת הרוטב", "בישול הפסטה", "חיבור והתאמת סמיכות"],
        None,
    ),
    (
        "fish",
        "דגים",
        {"דג", "דגים", "סלמון", "טונה", "בקלה", "fish", "salmon", "cod", "tuna"},
        "דגים נבדלים בעובי ובתכולת השומן. בחר שיטת הכנה לפי הנתח ולא רק לפי שם המנה, ועקוב אחר מרקם במהלך ההכנה.",
        ["איזה דג ומה עובי הנתח?", "צלייה, מחבת או בישול ברוטב?"],
        ["הכנת הנתח", "בישול בשיטה שבחרת", "בדיקת מוכנות"],
        63,
    ),
    (
        "meat",
        "בשר",
        {"בשר", "בקר", "כבש", "כתף", "אסאדו", "צלי", "סטייק", "beef", "lamb", "steak", "meat"},
        "נתח עדין ונתח עשיר ברקמת חיבור דורשים גישה שונה. נתחים קשים מתאימים לעיתים לבישול ממושך בנוזל; נתח עדין אינו דורש אותו תהליך.",
        ["מה שם הנתח, והאם מדובר בבשר טחון או בנתח שלם?", "מה המרקם שאתה רוצה לקבל?"],
        ["זיהוי הנתח", "הכנה לפי השיטה שבחרת", "בדיקת מוכנות לפי סוג הבשר"],
        None,
    ),
    (
        "eggs",
        "מנות ביצים",
        {"ביצים", "ביצה", "שקשוקה", "חביתה", "פריטטה", "eggs", "egg", "omelet", "shakshuka"},
        "במנות ביצים חשוב להבחין בין מרקם הרוטב למצב הביצים. הזמן אינו מחליף בדיקה של הביצים עצמן.",
        ["האם הביצים שלמות או חלק מתערובת?", "מה כבר מוכן במנה?"],
        ["הכנת הבסיס", "הוספת הביצים", "בדיקת הביצים"],
        None,
    ),
    (
        "grains",
        "אורז ודגנים",
        {"אורז", "בורגול", "קוסקוס", "קינואה", "rice", "couscous", "quinoa"},
        "סוג הדגן משפיע על כמות הנוזל ועל אופן ההכנה. התחל מהוראות האריזה והתאם לפי מצב הסיר, בלי להעתיק יחס נוזלים מסוג אחר.",
        ["באיזה סוג דגן אתה משתמש?", "מה כבר הוספת לסיר?"],
        ["בדיקת הוראות האריזה", "בישול ובדיקת נוזלים", "בדיקת מרקם"],
        None,
    ),
    (
        "vegetables",
        "ירקות",
        {"ירקות", "ירק", "תפוחי", "גזר", "קישוא", "ברוקולי", "כרובית", "vegetables", "potatoes", "carrot"},
        "מבנה הירק ותכולת המים משפיעים על ההתנהגות בחום. חיתוך דומה בגודל מסייע לקבלת תוצאה אחידה יותר; בחר אם המטרה היא השחמה או ריכוך.",
        ["אילו ירקות ובאיזה גודל חיתוך?", "אתה רוצה השחמה או תוצאה רכה יותר?"],
        ["חיתוך", "הכנה בשיטה שבחרת", "בדיקת מרקם"],
        None,
    ),
    (
        "soup",
        "מרקים ותבשילים",
        {"מרק", "תבשיל", "קדרה", "soup", "stew"},
        "בתבשיל בנוזל, סדר ההוספה תלוי בזמן הריכוך של המרכיבים. בדוק בנפרד מרקם, סמיכות ותיבול; מרכיבים שונים אינם מוכנים בהכרח יחד.",
        ["אילו מרכיבים יש בתבשיל?", "מה כבר נמצא בסיר ומה עדיין בחוץ?"],
        ["הכנת בסיס", "הוספת מרכיבים", "בדיקת סמיכות ומרקם"],
        None,
    ),
]


def dish_context(title, method="", ingredients=()):
    linked = graph_context(title, method, ingredients)
    normalized_title = re.sub(r"(?:ללא|בלי|without)\s+\w+", "", title.lower())
    title_words = set(re.findall(r"[^\W_]+", normalized_title))
    ingredient_words = set(re.findall(r"[^\W_]+", " ".join(ingredients).lower()))
    head_words = set(re.findall(r"[^\W_]+", re.split(r"\s+(?:עם|with)\s+", normalized_title)[0]))
    matches = [family for family in FAMILIES if head_words & family[2]] or [
        family for family in FAMILIES if title_words & family[2]
    ]
    # Title determines the dish family. Ingredients supply missing context but do not turn
    # e.g. a pasta dish with chicken into an assumed standalone chicken roast.
    family = (
        min(
            matches,
            key=lambda entry: min(
                (
                    index
                    for index, token in enumerate(re.findall(r"[^\W_]+", normalized_title))
                    if token in entry[2]
                ),
                default=10000,
            ),
        )
        if matches
        else next((entry for entry in FAMILIES if ingredient_words & entry[2]), None)
    )
    if family is None and linked["ingredients"]:
        categories = {node["category"] for node in linked["ingredients"]}
        if "עופות" in categories:
            family = FAMILIES[0]
        elif categories & {"בקר", "טלה"}:
            family = FAMILIES[3]
        elif any("דגים" in category for category in categories):
            family = FAMILIES[2]
        elif any(category.startswith("ירקות") or category == "פטריות" for category in categories):
            family = FAMILIES[6]
        elif "קטניות" in categories:
            family = (
                "legumes",
                "קטניות",
                set(),
                "ברר אם הקטניות יבשות או מוכנות ופעל לפי הוראות מתאימות.",
                ["האם מדובר בקטניות יבשות, משומרות או מבושלות?"],
                ["בדיקת סוג המוצר", "הכנה לפי הוראות המוצר"],
                None,
            )
        elif categories & {"מוצרי חלב", "גבינות"}:
            family = (
                "dairy",
                "מוצרי חלב",
                set(),
                "בחר טיפול לפי סוג המוצר והמנה.",
                ["מה סוג המוצר ומה התוצאה הרצויה?"],
                ["הכנת המוצר", "שילוב במנה לפי בחירתך"],
                None,
            )
    tips, questions, suggestions, minimum = [], [], [], None
    if family:
        key, label, _, text, questions, suggestions, minimum = family
        tips.append(ContextTip(title="עיקרון שמתאים לסוג המנה", text=text, source=TECHNIQUE))
    else:
        key, label = "general", "הכנה כללית"
        questions = ["מהם חומרי הגלם המרכזיים?", "איזו שיטת הכנה אתה מתכנן?"]
        suggestions = ["הכנת חומרי הגלם", "הפעולה שבחרת", "בדיקת התוצאה"]
        tips.append(
            ContextTip(
                title="מתחילים מהתוצאה הרצויה",
                text="ספר מה חומרי הגלם ומה תרצה להשיג. אפשר לתכנן את השלבים שלך, גם כשהמנה אינה מופיעה במאגר.",
                source=TECHNIQUE,
            )
        )
    # Safety follows every known protein in the dish, including mixed dishes.
    all_words = title_words | ingredient_words
    if all_words & FAMILIES[0][2]:
        minimum = 74
        tips.append(
            ContextTip(
                title="בדיקה לעוף ולהודו",
                text="בנתחי עוף והודו נדרשת מדידה של לפחות 74°C בחלקים העבים, בלי נגיעה בעצם. צבע או זמן אינם תחליף למדידה.",
                source=SAFETY,
            )
        )
    elif minimum == 63:
        tips.append(
            ContextTip(
                title="בדיקת דג",
                text="סף הטמפרטורה לדג הוא 63°C. המדידה וההתאמה לנתח נפרדות מהחלטה על מרקם או רוטב.",
                source=SAFETY,
            )
        )
    if method:
        tips.append(
            ContextTip(
                title="השיטה שבחרת",
                text=f"שיטת ההכנה שדיווחת: {method}. בדוק את מצב המזון בפועל; בחירת שיטה אינה מספקת לקביעת זמן או טמפרטורת תנור בלי פרטי המנה.",
                source=TECHNIQUE,
            )
        )
        questions = [
            question for question in questions if not any(term in question for term in ("שיטת", "צלייה,"))
        ]
    if {"הודו", "turkey"} & title_words and {"כנפי", "כנפיים", "wings", "wing"} & title_words:
        tips.insert(
            0,
            ContextTip(
                title="כנפי הודו — שתי גישות אפשריות",
                text="אפשר לצלות כנפי הודו בתבנית פתוחה עם מעט שמן, או להשחים ואז לבשל מכוסה עם נוזל. בחר לפי התוצאה שאתה רוצה; אין צורך להיצמד למתכון היחיד של המערכת. הוראות יצרן הן נקודת ייחוס, והזמן דורש התאמה לנתחים ולכמות.",
                source="https://www.butterball.com/products/turkey-cuts/wings",
            ),
        )
    if ingredients:
        questions = [
            question
            for question in questions
            if "חומרי הגלם" not in question and "אילו מרכיבים" not in question
        ]
    questions = questions or ["מה מצב המנה כרגע?"]
    # Explicit gizzards do not need the ambiguous archive label's liver question.
    gizzards = any(node["id"] == "chicken_giblets" for node in linked["ingredients"]) and bool(
        (title_words | ingredient_words) & {"קורקבנים", "קורקבן", "קוקבנים", "קוקבן", "gizzards", "gizzard"}
    )
    if gizzards:
        questions = [
            "הקורקבנים טריים או קפואים, והאם הם כבר מופשרים ומנוקים?",
            "אתה רוצה תבשיל רך ברוטב, או השחמה בסיום?",
            "מה כבר עשית, ומה הכמות שיש לך?",
        ]
        if not method:
            questions.insert(1, "באיזו שיטה תרצה להכין — בישול בנוזל, סיר לחץ או מחבת?")
    adapted = []
    for node in linked["ingredients"][:3]:
        tip_text = node["tip"]
        if gizzards and node["id"] == "chicken_giblets":
            tip_text = (
                "לפני שמתחילים בדוק אם הקורקבנים מופשרים ומנוקים ושמור אותם בקירור עד ההכנה. "
                "אם המטרה תוצאה רכה ברוטב, אפשר לבחור בישול בנוזל או סיר לחץ ולבדוק רכות במהלך העבודה; השחמה אפשר לשקול בנפרד. "
                "אין לקבוע זמן אחיד בלי לדעת את הכמות, מצב חומר הגלם ושיטת ההכנה."
            )
        adapted.append(
            ContextTip(
                title="קורקבנים" if gizzards and node["id"] == "chicken_giblets" else node["name"],
                text=tip_text,
                source="",
                origin="USER_GRAPH_ADAPTED",
                source_ids=[node["source_id"]],
            )
        )
        if node["clarification"] and not (gizzards and node["id"] == "chicken_giblets"):
            questions.insert(0, node["clarification"])
    tips = adapted + tips
    if linked["minimum_temperature"] is not None:
        minimum = max(minimum or 0, linked["minimum_temperature"])
        rest = linked["rest_seconds"]
        safety_text = f"סף הבישול הכללי לחומרי הגלם שזוהו: {minimum:g}°C."
        if rest:
            safety_text += " לנתחי הבשר השלמים נדרשת גם מנוחה של 3 דקות; מדידה לבדה אינה מאמתת אותה."
        safety_text += " אין להשתמש בטמפרטורת המרקם שבמסמך כאישור בטיחות."
        tips.insert(
            0,
            ContextTip(
                title="בדיקת בטיחות נפרדת ממרקם",
                text=safety_text,
                source=SAFETY,
                origin="SAFETY_POLICY",
                source_ids=["safety_policy"],
            ),
        )
    if linked["method"]:
        selected = linked["method"]
        tips.append(
            ContextTip(
                title=selected["name"],
                text=selected["advice"],
                source="",
                origin="USER_GRAPH_ADAPTED",
                source_ids=["cooking_methods/" + selected["id"]],
            )
        )
        suggestions = list(dict.fromkeys([*selected["suggestions"], *suggestions]))[:12]
    tips = adapted[:1] + [tip for tip in tips if tip not in adapted[:1]]
    tips = tips[:8]
    return DishContext(
        family=key,
        label=label,
        method=method,
        identified=family is not None,
        tips=tips,
        questions=questions,
        suggestions=suggestions,
        minimum_temperature=minimum,
        sources=list(dict.fromkeys(tip.source for tip in tips if tip.source)),
        graph=linked,
        minimum_rest_seconds=linked["rest_seconds"],
    ).model_dump()


def contextual_reply(context, text, current_title="", consultant=False):
    """Return advice and an issue label. Never infer completion from a free-text report."""
    value = text.lower()
    if value in ("יש בעיה", "צריך עזרה"):
        return "מה השתבש — חום, צבע, מרקם, סמיכות או תיבול? תאר מה קרה ואציע בדיקה שמתאימה למצב.", ""
    if any(term in value for term in ("סמיך מדי", "סמיכה מדי", "too thick")):
        return (
            "אם מדובר ברוטב, אפשר להוסיף מעט נוזל מתאים בהדרגה ולערבב. בפסטה אפשר להשתמש במעט ממי הבישול. בדוק שוב סמיכות ותיבול אחרי כל תוספת.",
            "סמיכות הרוטב",
        )
    if any(term in value for term in ("דליל מדי", "נוזלי מדי", "too thin")):
        return (
            "אם הרוטב מתאים לבישול, אפשר לרכז אותו בבעבוע עדין ולבדוק לעיתים קרובות. לפני שינוי אחר, ספר מה מרכיבי הרוטב.",
            "רוטב דליל",
        )
    if any(term in value for term in ("נשרף", "שרוף", "נדבק", "burnt", "burned", "sticking")):
        return (
            "לפי הדיווח יש חשש לחריכה. הפחת חום אם בטוח לעשות זאת ובדוק אם יש חלקים שחורים או ריח שרוף. אל תערבב חלקים שרופים לתוך שאר המנה.",
            "חריכה או הידבקות",
        )
    if any(term in value for term in ("מלוח מדי", "יותר מדי מלח", "too salty")):
        return (
            "אל תוסיף עוד מלח כרגע. מה סוג המנה וכמה כבר הוספת? דרך התיקון תלויה במרכיבים ובאפשרות להגדיל את הכמות בלי מלח.",
            "תיבול",
        )
    if "שום" in value or "garlic" in value:
        return (
            "אם אתה מטגן שום קצוץ, עקוב אחר הצבע והריח; הוא עלול להיחרך מהר. אפשר להפחית חום לפני ההוספה, בהתאם למנה.",
            "",
        )
    if "בצל" in value or "onion" in value or "בצל" in current_title:
        if "למה" in value or "why" in value:
            return (
                "ריכוך והשחמת הבצל הם מטרות שונות. מידת ההשחמה הרצויה תלויה במנה שאתה בוחר להכין; בצל שקוף אינו בהכרח טעות.",
                "",
            )
        if "זהוב" in value and not re.search(r"לא\s+(?:ממש\s+)?זהוב", value):
            return (
                "לפי הדיווח הבצל זהוב. אם זה הצבע והמרקם שרצית למנה, אפשר לבחור את הפעולה הבאה; אין צורך להמשיך להשחים רק בגלל טיימר.",
                "",
            )
        if "שקוף" in value:
            return (
                "לפי הדיווח הבצל שקוף. זה עשוי להתאים למנה שמטרתה ריכוך בלי השחמה; הבחירה אם להמשיך תלויה בתוצאה שאתה רוצה.",
                "",
            )
        return (
            "לפי הדיווח אתה עובד עם בצל. אם הוא משחים לפני שהוא מתרכך, אפשר להפחית חום. מה מצבו עכשיו — לבן, שקוף, זהוב או כהה מדי?",
            "",
        )
    if context["minimum_temperature"] is not None and any(
        term in value for term in ("מוכן", "מוכנה", "בטוח", "done", "safe")
    ):
        return (
            f"לא ניתן לקבוע מוכנות לפי התיאור בלבד. למרכיב הזה נדרשת מדידה של לפחות {context['minimum_temperature']:g}°C. אפשר לדווח מדידה באזור העבודה.",
            "",
        )
    if any(term in value for term in ("למה", "why", "הסבר", "עצה", "המלצה")):
        return context["tips"][0]["text"], ""
    if text == "המנה נראית טוב":
        return "רשמתי שלפי הדיווח שלך המנה נראית טוב. הבחירה אם להמשיך, לשנות או לסיים נשארת שלך.", ""
    tip = context["tips"][0]["text"]
    return (tip if consultant else tip + " " + context["questions"][0]), ""
