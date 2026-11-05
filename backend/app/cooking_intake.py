"""Explicit dish interview and coverage gaps. Source text is stored, never executed."""

from typing import Literal
from urllib.parse import urlencode, urlsplit

from pydantic import Field, field_validator

from app.schemas import StrictModel


class IntakeFacts(StrictModel):
    family: str = Field(default="", pattern="^(|meat|fish|vegetables|starch|legumes|eggs|soup|other)$")
    main_ingredient: str = Field(default="", max_length=160)
    protein: str = Field(default="", pattern="^(|chicken|turkey|beef|other)$")
    cut: str = Field(default="", max_length=160)
    quantity: str = Field(default="", max_length=160)
    goal: str = Field(default="", pattern="^(|sauce|brown|soft|crisp|other)$")
    equipment: str = Field(default="", pattern="^(|pot|pan|oven|grill|steamer|pressure|other)$")
    method: str = Field(default="", max_length=160)
    oven_temperature: int = Field(default=200, ge=100, le=250)
    estimated_minutes: int = Field(default=45, ge=1, le=240)
    oven_program: str = Field(default="טורבו", pattern="^(טורבו|חום עליון ותחתון)$")
    defaults_edited: list[Literal["temperature", "minutes", "program"]] = Field(default_factory=list, max_length=3)
    recipe_url: str = Field(default="", max_length=2000)
    recipe_text: str = Field(default="", max_length=10000)

    @field_validator("recipe_url")
    @classmethod
    def public_reference(cls, value):
        value = value.strip()
        if value:
            parsed = urlsplit(value)
            if (
                parsed.scheme not in ("http", "https")
                or not parsed.hostname
                or parsed.username
                or parsed.password
            ):
                raise ValueError("Use an http(s) recipe link without credentials")
        return value


FAMILIES = {
    "meat": "בשר ועוף",
    "fish": "דגים",
    "vegetables": "ירקות",
    "starch": "אורז, פסטה ודגנים",
    "legumes": "קטניות",
    "eggs": "ביצים",
    "soup": "מרקים ותבשילים",
    "other": "משפחה אחרת",
}
PROTEINS = {"chicken": "עוף", "turkey": "הודו", "beef": "בקר", "other": "סוג אחר"}
GOALS = {"sauce": "תבשיל ברוטב", "brown": "השחמה", "soft": "רך", "crisp": "פריך", "other": "תוצאה אחרת"}
EQUIPMENT = {
    "pot": "סיר רגיל",
    "pan": "מחבת",
    "oven": "תנור",
    "grill": "גריל",
    "steamer": "סיר אידוי",
    "pressure": "סיר לחץ",
    "other": "כלי אחר",
}

FAMILY_GUIDANCE = {
    "soup": "סדר ההוספה לסיר תלוי במרכיבים: הכן קודם רשימה של מה שנכנס ומתי. בדוק בנפרד את רכות החתיכות ואת סמיכות הנוזל. אם יש בשר, עוף או דג, צריך גם בדיקת מוכנות שמתאימה להם.",
    "meat": "בבשר ועוף נברר קודם את סוג הבשר והנתח. נתח רך ונתח לתבשיל דורשים טיפול שונה. הכן כלים נפרדים למזון נא וכלי נקי להגשה; אל תבחר זמן בישול לפני שנדע מה הנתח והגודל.",
    "fish": "שמור את הדג בקירור בזמן ההכנות. ברר אם הוא מופשר ומה עובי החלק העבה. הכן תיבול, כלי הגשה נקי ומדחום לפני החימום; עובי וצורת הנתח משפיעים על קצב הבישול.",
    "vegetables": "חתוך חתיכות בגודל דומה כדי שיתרככו באופן אחיד. כשמשלבים ירקות שונים, הוסף את הקשים לפני הרכים. בדוק במזלג חתיכה גדולה והשווה למרקם שרצית.",
    "starch": "ברר איזה דגן או סוג פסטה יש לך, ומדוד את הכמות היבשה. הכן נוזל וכלי לפי הוראות האריזה או המתכון; יחס מים שמתאים לאורז אחד לא בהכרח מתאים לאחר.",
    "legumes": "ברר אם הקטניות יבשות, משומרות או כבר מבושלות. לקטניות יבשות פעל לפי הוראות המוצר המתאימות לסוגן; אין להחליף אותן במשומרות עם אותם זמני בישול.",
    "eggs": "בחר אם המטרה ביצים שלמות, חביתה או תערובת. הכן מראש את הכלים והמרכיבים, ושבור ביצים לכלי נפרד כדי לבדוק אותן לפני שילוב במנה.",
    "other": "אפשר להתחיל בסידור המרכיבים והכלים. הבא מתכון או תאר לאיזו מנה זה דומה, מה המרכיב המרכזי ומה המרקם שתרצה; עד אז נבחר רק פעולות שמתאימות בוודאות.",
    "": "לאיזו משפחה המנה דומה? בחר משפחה, ואז נברר חומר גלם, כמות ותוצאה רצויה. בינתיים אפשר להכין משטח עבודה נקי ולרכז את המרכיבים, בלי להתחיל חימום לא מתוכנן.",
}


def resolved_family(state):
    facts = state.get("intake_facts", {})
    if facts.get("family"):
        return facts["family"]
    from app.station_protocol import identify

    _profile, known_family = identify(state["dish_title"])
    if known_family:
        return known_family
    family = state["context"].get("family", "")
    return {
        "poultry": "meat",
        "meat": "meat",
        "beef": "meat",
        "fish": "fish",
        "vegetables": "vegetables",
        "vegetable": "vegetables",
        "grains": "starch",
        "pasta": "starch",
        "rice": "starch",
        "legumes": "legumes",
        "eggs": "eggs",
        "soup": "soup",
    }.get(family, "")


def classification_ingredients(facts):
    """Reported classification supplements context without rewriting the ingredient list."""
    reported = [facts["main_ingredient"]] if facts.get("main_ingredient", "").strip() else []
    if facts.get("family") == "meat":
        return reported + (
            [PROTEINS[facts["protein"]]] if facts.get("protein") in ("chicken", "turkey", "beef") else []
        )
    aliases = {"fish": "דג", "vegetables": "ירקות", "starch": "דגנים", "legumes": "קטניות", "eggs": "ביצים"}
    return reported + ([aliases[facts["family"]]] if facts.get("family") in aliases else [])


def attach_intake(state):
    facts = IntakeFacts.model_validate(state.get("intake_facts", {})).model_dump()
    from app.method_policy import canonical_method
    method_id = canonical_method(state.get('method', '') or state['dish_title'])
    if method_id == 'grill_direct':
        facts['method'] = 'grill_direct'
        if facts['equipment'] in ('', 'pot'):
            facts['equipment'] = 'grill'
        if facts['goal'] in ('', 'sauce'):
            facts['goal'] = 'brown'
    if not facts['protein']:
        title = state['dish_title'].lower()
        for word, protein in [('עוף','chicken'),('chicken','chicken'),('הודו','turkey'),('turkey','turkey'),('בקר','beef'),('beef','beef')]:
            if word in title:
                facts['protein'] = protein
                break
    if facts['protein'] == 'chicken' and method_id == 'oven_roast':
        facts['equipment'] = facts['equipment'] or 'oven'
        facts['goal'] = facts['goal'] or 'brown'
    state["intake_facts"] = facts
    family = resolved_family(state)
    if facts['protein'] and family == 'meat' and not facts['family']:
        facts['family'] = 'meat'
    # A user-written step or a generic graph path is not a complete recipe.
    authored = any(
        step.get("source", "").startswith("CHEF_AUTHORED:salmon") for step in state["custom_steps"]
    )
    authored = authored or bool(state.get('recipe_snapshot'))
    supplied = bool(facts["recipe_text"].strip() or facts["recipe_url"])
    missing = []

    def need(key, label, why, choices=None):
        missing.append({"key": key, "label": label, "why": why, "choices": choices or {}})

    if not family:
        need("family", "לאיזו משפחה המנה שייכת?", "כדי לבחור פעולות שמתאימות לחומר הגלם", FAMILIES)
    if (
        not facts["main_ingredient"].strip()
        and not state["ingredients"]
        and family not in ("meat", "fish", "eggs")
    ):
        need(
            "main_ingredient",
            "מהם חומרי הגלם המרכזיים?",
            "למשל גזר ותפוח אדמה, או אורז מלא; כדי לבחור טיפול שמתאים להם",
        )
    if family == "meat" and not facts["protein"]:
        text = " ".join([state["dish_title"], *state["ingredients"]])
        inferred = next((key for key, label in PROTEINS.items() if key != "other" and label in text), "")
        if not inferred:
            need("protein", "איזה בשר יש לך?", "עוף, הודו ובקר דורשים התאמה שונה", PROTEINS)
    if family in ("meat", "fish") and not facts["cut"].strip():
        need(
            "cut",
            "איזה נתח, מה הגודל והאם שלם או חתוך?",
            "כדי להתאים ריכוך וחימום; למשל חזה עוף חתוך או כתף בקר בקוביות",
        )
    if not facts["quantity"].strip():
        need("quantity", "מה הכמות?", "למשל 500 גרם, שתי כוסות יבשות או ארבע מנות; כדי להתאים כמויות וכלי")
    if not facts["goal"]:
        need("goal", "איזו תוצאה אתה רוצה?", "כדי לבחור בין ריכוך, השחמה ופריכות", GOALS)
    if not facts["equipment"]:
        need("equipment", "באיזה כלי תשתמש?", "כדי להתאים את סדר הפעולות והשליטה בחום", EQUIPMENT)
    if not state["method"]:
        need("method", "באיזו שיטת הכנה?", "בחר שיטה מתוך ההמלצות כדי להתאים את פעולות החימום")
    gaps = []
    if not authored:
        gaps.append(
            {
                "key": "recipe",
                "text": "אין כאן עדיין מתכון מלא עם כמויות וסדר עבודה למנה שלך.",
                "next": "פתח מתכון מתאים בקישורי החיפוש. אפשר לשמור אותו לעיון; ההכוונה כאן נשענת על הבחירות המובנות שלך.",
            }
        )
    if supplied and not state.get('recipe_snapshot'):
        gaps.append(
            {
                "key": "source_review",
                "text": "המתכון שסיפקת נשמר לעיון; הוא עדיין לא הומר לפעולות מובנות.",
                "next": "בחר פעולה ממאגר הפעולות לפי השלב במתכון. אם חסרה פעולה, ציין מה היא ומה מצופה בה.",
            }
        )
    if not missing and not authored:
        gaps.append(
            {
                "key": "procedure",
                "text": "פרטי המנה ברורים יותר, אך אין עדיין תהליך בדוק שמתאים לשילוב הזה.",
                "next": "החומר החסר הוא מתכון עם רשימת מרכיבים וכמויות, חום, סדר פעולות וסימני בדיקה. זמן חימום לבדו אינו מספיק.",
            }
        )
    query = {
        "meat": {"chicken": "chicken", "turkey": "turkey", "beef": "beef"}.get(facts["protein"], "meat"),
        "fish": "fish",
        "vegetables": "vegetables",
        "starch": "rice pasta",
        "legumes": "beans lentils",
        "eggs": "eggs",
        "soup": "soup",
    }.get(family, "recipes")
    exact_query = state["dish_title"] or facts["main_ingredient"].strip()
    if exact_query in ("מנה לבחירה", ""):
        exact_query = FAMILIES.get(family, "מנה")
    search_links = [
        {"label": "חיפוש מתכונים בעברית: " + exact_query, "url": "https://www.google.com/search?" + urlencode({"q": exact_query + " מתכון"})},
        {"label": "חיפוש ב־השולחן", "url": "https://www.google.com/search?" + urlencode({"q": "site:hashulchan.co.il " + exact_query + " מתכון"})},
        {"label": "חיפוש ב־mako אוכל", "url": "https://www.google.com/search?" + urlencode({"q": "site:mako.co.il/food " + exact_query + " מתכון"})},
    ]
    if "קורקבנ" in exact_query:
        search_links.insert(0, {"label": "קורקבנים עם פטריות — אמהות מבשלות ביחד", "url": "https://imaot.co.il/Book/Page/168585"})
        search_links.insert(1, {"label": "קורקבנים ולבבות הודו — וואלה אוכל (מנה דומה)", "url": "https://food.walla.co.il/recipe/1649"})
    specific = PROTEINS.get(facts['protein']) or facts['main_ingredient']
    guidance = FAMILY_GUIDANCE[family]
    if specific:
        guidance = "הכן את המרכיבים והכלים לפני תחילת העבודה."
    if facts['protein'] == 'chicken':
        guidance = "ייבש את העוף לפני התיבול; מדוד 74°C בחלק העבה לפני ההגשה."
    defaults = {}
    if facts['protein'] == 'chicken' and method_id == 'oven_roast':
        defaults = {"temperature": facts['oven_temperature'], "program": facts['oven_program'],
                    "minutes": facts['estimated_minutes'], "equipment": "תבנית תנור",
                    "assumption": "נקודת התחלה לנתחי עוף מופשרים; לעוף שלם יש להתאים לפי משקל."}
    from app.practical_knowledge import cooking_defaults

    indexed = cooking_defaults(state["dish_title"], method_id) if family in ("", "other", "vegetables") else {}
    if indexed and not state.get("recipe_snapshot"):
        defaults = indexed
        if "temperature" in facts["defaults_edited"]:
            defaults["temperature"] = facts["oven_temperature"]
        if "minutes" in facts["defaults_edited"]:
            defaults["minutes"] = facts["estimated_minutes"]
        if "program" in facts["defaults_edited"]:
            defaults["program"] = facts["oven_program"]
    state["intake_guidance"] = {
        "defaults": defaults,
        "recipe_search_links": search_links,
        "family": family,
        "family_label": specific or FAMILIES.get(family, "טרם נבחרה משפחה"),
        "guidance": guidance,
        "goal_choices": {key: value for key, value in GOALS.items() if key != 'sauce' or method_id not in ('grill_direct', 'oven_roast', 'pan_sear')},
        "main_ingredient_needed": not state['context'].get('identified') and not facts['protein'],
        "missing": missing,
        "knowledge_gaps": gaps,
        "recipe_requested": not authored and not supplied,
        "recipe_status": "imported" if state.get('recipe_snapshot') else "supplied_unreviewed" if supplied else "authored" if authored else "missing",
        "recipe_search_url": "https://www.bbcgoodfood.com/search?" + urlencode({"q": query}),
    }
    from app.station_protocol import attach_station

    protocol = attach_station(state)
    state["intake_guidance"]["guidance"] = protocol["text"]
    state["intake_guidance"]["recommended_reading"] = protocol["recommended_reading"]
    state["intake_guidance"]["knowledge_gap_flagged"] = protocol["knowledge_gap_flagged"]
    for gap in gaps:
        gap["next"] = "Knowledge Base Extension Needed — " + protocol["blocks"][5]["text"]
    state["intake_guidance"]["knowledge_gaps"] = gaps + [
        {"key": "station", "text": "Knowledge Base Extension Needed", "next": gap}
        for gap in protocol["gaps"]
    ]
    if family in ("fish", "meat"):
        for item in missing:
            if item["key"] == "cut":
                item["label"] = f"איזה נתח של {state['dish_title']} ומה עוביו בס״מ?"
                item["why"] = "כדי להתאים את החימום לנתח ולעובי של המנה הזו"
    if missing and missing[0]["key"] == "family":
        missing[0]["label"] = protocol["next_question"]


def intake_reply(state):
    info = state["intake_guidance"]
    if state.get("station_protocol"):
        return state["station_protocol"]["text"]
    parts = [info["guidance"]]
    if info["missing"]:
        first = info["missing"][0]
        parts.append(first["label"] + " " + first["why"] + ".")
    elif info["knowledge_gaps"]:
        parts.append(info["knowledge_gaps"][-1]["next"])
    return "\n\n".join(parts)
