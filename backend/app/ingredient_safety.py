"""Shared checks of declared ingredients, not certification of product composition."""
import re
import unicodedata

from app.knowledge import DomainError


GROUPS = {
    "milk": ("milk", "dairy", "cheese", "butter", "cream", "yogurt", "whey", "חלב", "גבינה", "גבינות", "חמאה", "שמנת", "יוגורט", "מי גבינה"),
    "eggs": ("egg", "eggs", "ביצה", "ביצים"),
    "wheat": ("wheat", "gluten", "flour", "חיטה", "קמח חיטה", "גלוטן"),
    "fish": ("fish", "salmon", "cod", "tuna", "nile perch", "דג", "דגים", "סלמון", "טונה", "בקלה", "נסיכת הנילוס"),
    "peanuts": ("peanut", "peanuts", "בוטן", "בוטנים"),
    "sesame": ("sesame", "tahini", "שומשום", "טחינה"),
    "soy": ("soy", "soya", "tofu", "סויה", "טופו"),
    "tree_nuts": ("tree nuts", "nuts", "walnut", "walnuts", "almond", "almonds", "cashew", "cashews", "hazelnut", "hazelnuts", "pecan", "pecans", "pistachio", "pistachios", "אגוזים", "אגוזי מלך", "אגוז מלך", "שקד", "שקדים", "קשיו", "אגוזי לוז", "פקאן", "פיסטוק", "פיסטוקים"),
    "shellfish": ("shellfish", "shrimp", "shrimps", "prawn", "prawns", "crab", "lobster", "פירות ים", "שרימפס", "סרטן", "סרטנים", "לובסטר"),
    "molluscs": ("shellfish", "mollusc", "molluscs", "mussel", "mussels", "oyster", "oysters", "squid", "פירות ים", "צדפה", "צדפות", "קלמארי", "דיונון"),
}
MEAT = ("meat", "beef", "chicken", "turkey", "lamb", "בשר", "בקר", "עוף", "הודו", "כבש", "שוק בקר")
PLANT_DAIRY = ("almond milk", "soy milk", "oat milk", "coconut milk", "חלב שקדים", "חלב סויה", "חלב שיבולת שועל", "חלב קוקוס", "שמנת צמחית")
UNKNOWN_COMPOUNDS = ("רוטב מוכן", "תערובת מוכנה", "תערובת תבלינים", "תחליף שמנת", "prepared sauce", "seasoning mix", "cream substitute")


def normalize(value):
    text = unicodedata.normalize("NFKC", str(value)).casefold()
    text = re.sub(r"[\u0591-\u05bd\u05bf-\u05c7]", "", text)
    return " ".join(re.sub(r"[^\w]+", " ", text).split())


def contains(text, phrase):
    return bool(re.search(r"(?<!\w)" + re.escape(normalize(phrase)) + r"(?!\w)", normalize(text)))


def ingredient_groups(name):
    result = {group for group, aliases in GROUPS.items() if any(contains(name, alias) for alias in aliases)}
    if any(contains(name, phrase) for phrase in PLANT_DAIRY):
        result.discard("milk")
    return result


def check_ingredients(ingredients, avoided=(), forbid_meat_dairy=False):
    names = [str(name).strip() for name in ingredients if str(name).strip()]
    avoid = [str(name).strip() for name in avoided if str(name).strip()]
    forbidden_groups = set().union(*(ingredient_groups(value) for value in avoid)) if avoid else set()
    for name in names:
        if ingredient_groups(name) & forbidden_groups or any(contains(name, value) for value in avoid):
            raise DomainError("ALLERGEN_CONFLICT", f"עצור: {name} מתנגש עם אלרגיה שדיווחת. אל תשתמש ברכיב ואל תגיש אותו; בחר חלופה מתאימה.", 422)
    if avoid and any(contains(name, phrase) for name in names for phrase in UNKNOWN_COMPOUNDS):
        raise DomainError("INGREDIENT_COMPOSITION_UNKNOWN", "לפני השימוש במוצר המוכן, בדוק את רשימת הרכיבים והאזהרות על התווית מול האלרגיות שלך. אין כאן מספיק מידע על הרכבו.", 422)
    if forbid_meat_dairy:
        has_meat = any(contains(name, term) for name in names for term in MEAT)
        has_dairy = any("milk" in ingredient_groups(name) for name in names)
        if has_meat and has_dairy:
            raise DomainError("MEAT_DAIRY_CONFLICT", "בחרת הפרדה בין בשר לחלב, אבל במנה יש רכיבים משתי הקבוצות. החלף את הרכיב החלבי; אם בוחרים תחליף צמחי, בדוק את התווית לפני השימוש.", 422)
