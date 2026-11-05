"""Additive, attributed book knowledge for the cooking coach."""

import json
import re
from functools import lru_cache

import yaml

from app.ontology_bridge import DEFAULT_VAULT_ROOT, load_ontology
from app.retrieval import semantic_concepts, tokens


def food_domains(text):
    from app.ingredient_safety import contains
    aliases = {"fish": ("fish", "finfish", "salmon", "דג", "דגים", "סלמון"),
               "eggs": ("egg", "eggs", "ביצה", "ביצים")}
    return {key for key, values in aliases.items() if any(contains(text, value) for value in values)}


def background_excerpt(body):
    """Read a note's explanatory summary only, never execute its rule parameters."""
    match = re.search(r"^##\s+(?:תקציר הידע|תקציר|Summary)\s*\n+(.+?)(?=\n\s*\n|\n##|\Z)", body, re.M | re.S)
    return re.sub(r"[*`]", "", match.group(1)).strip()[:1000] if match else ""


def technique_domains(text):
    from app.ingredient_safety import contains
    return {"poaching"} if any(contains(text, value) for value in ("שליקה", "שליקת", "poach", "poaching")) else set()

# Application guidance derived from the notes; provenance remains in source/source_ids.
PRACTICAL_TIPS = {
    "EVD-FLB-CH03-003": (
        "מתי לבשל קצר ומתי להמשיך עד לריכוך?",
        ("נתח רך כמו פילה צריך בעיקר להגיע למידת העשייה הרצויה; חימום ממושך עלול לייבש אותו. "
        "נתח עשיר ברקמת חיבור, כמו כתף לתבשיל, צריך גם זמן כדי להתרכך. "
        "בתבשיל כזה שמור על בעבוע עדין ונוזל בסיר, ובדוק במזלג: אם הבשר עדיין מתנגד, המשך ובדוק שוב. "
        "בדיקת הרכות ובדיקת טמפרטורת הבטיחות הן בדיקות נפרדות."),
    ),
    "EVD-MCG-RNG-CH05-002": (
        "איך לרכך ירקות שמיועדים לרוטב עגבניות",
        ("אם הירקות נשארים קשים ברוטב עגבניות, החומציות עלולה לעכב את הריכוך. "
        "דרך עבודה אפשרית: חתוך לחתיכות דומות, בשל במים בנפרד ובדוק במזלג את מרכז החתיכה הגדולה. "
        "כשהמזלג נכנס אך עדיין מורגשת מעט התנגדות, סנן והעבר לרוטב להשלמת הבישול. "
        "בדוק שוב במהלך הבישול ועצור במרקם שאתה רוצה; חתיכות קטנות מתרככות לפני גדולות. "
        "זו הצעת הכנה על בסיס העיקרון, ולא מתכון שמופיע בספר."),
    ),
    "RUL-MEAT-004": (
        "האם להמליח מראש, להשרות או לרכך?",
        ("להוספת טעם אפשר להשתמש במרינדה; היא משפיעה בעיקר על פני השטח. "
        "להמלחה מראש צריך להתאים כמות מלח ומשכה לנתח ולמתכון. "
        "לנתח קשה שמיועד לתבשיל, בישול ממושך בנוזל הוא דרך לריכוך. "
        "מה הנתח, מה משקלו ואיך תרצה לבשל אותו?"),
    ),
}


@lru_cache(maxsize=1)
def _snapshot(signature):
    return load_ontology(DEFAULT_VAULT_ROOT, include_source_pages=False)


def book_tips(query, *, limit=3):
    root = DEFAULT_VAULT_ROOT / "Culinary-Knowledge"
    try:
        signature = tuple(
            (str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in sorted(root.rglob("*.md"))
        )
        data = _snapshot(signature)
        manifest_path = root / "09_Sources" / "FoodLab-2015" / "FoodLab-2015-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
        enabled_claims = {record["id"] for record in manifest.get("records", [])}
        enabled_claim_ids = {record["claim_id"] for record in manifest.get("records", [])}
        mcgee_path = root / "09_Sources" / "McGee-2004-Supplied-Ranges" / "McGee-Ranges-manifest.json"
        mcgee_manifest = json.loads(mcgee_path.read_text(encoding="utf-8")) if mcgee_path.exists() else {}
        mcgee_claims = {record["id"] for record in mcgee_manifest.get("records", [])}
        mcgee_claim_ids = {record["claim_id"] for record in mcgee_manifest.get("records", [])}
        mcgee_rules = {record["id"] for record in mcgee_manifest.get("rules", [])}
    except (OSError, ValueError, yaml.YAMLError):
        return []
    q_tokens, q_concepts = tokens(query), semantic_concepts(query)
    query_domains = food_domains(query)
    ranked = []
    for node in data["nodes"]:
        meta = node["metadata"]
        primary_scope = " ".join([node["name"], node["title_he"], str(meta.get("title", "")), str(meta.get("chapter", "")), " ".join(meta.get("tags", []))])
        node_domains = food_domains(primary_scope)
        if query_domains and node_domains and query_domains.isdisjoint(node_domains):
            continue
        foodlab = node["id"] in enabled_claims and meta.get("source_text_checked") is True
        mcgee_checked = node["id"] in mcgee_claims and meta.get("source_text_checked") is True
        mcgee_rule = (
            node["id"] in mcgee_rules
            and meta.get("claim_type") == "INTERPRETATION"
            and bool(meta.get("source_claim_ids"))
            and set(meta["source_claim_ids"]) <= mcgee_claim_ids
        )
        rule = (
            node["id"] in {f"RUL-FLB-CH{i:02d}-001" for i in range(1, 10)}
            and meta.get("claim_type") == "INTERPRETATION"
            and bool(meta.get("source_claim_ids"))
            and set(meta["source_claim_ids"]) <= enabled_claim_ids
        )
        if (
            node["verification_status"] != "VERIFIED"
            and not foodlab
            and not rule
            and not mcgee_checked
            and not mcgee_rule
        ):
            continue
        refs = [
            s
            for s in meta.get("sources", [])
            if isinstance(s, dict) and s.get("source_id") in ("SRC-MCGEE-2004", "SRC-FOODLAB-2015")
        ]
        if not refs:
            continue
        # Background explanations only: never execute raw rule parameters, safety
        # thresholds, or arbitrary Markdown instructions as cooking commands.
        explanation = (
            meta.get("claim")
            if foodlab or mcgee_checked
            else meta.get("description") or meta.get("scientific_rationale") or background_excerpt(node["body"])
        )
        if rule or mcgee_rule:
            explanation = f"אם: {meta.get('if', '')}. אפשרויות: {meta.get('then', '')}. הסבר: {meta.get('because', '')}. פשרות: {meta.get('tradeoffs', '')}"
        if not isinstance(explanation, str) or not explanation.strip():
            continue
        searchable = " ".join([node["name"], node["title_he"], explanation, " ".join(meta.get("tags", []))])
        overlap = q_tokens & tokens(searchable)
        concepts = q_concepts & semantic_concepts(searchable)
        if not overlap and not concepts:
            continue
        score = len(overlap) + 2 * len(concepts) + 4 * len(technique_domains(query) & technique_domains(primary_scope))
        ref = refs[0]
        if ref["source_id"] == "SRC-FOODLAB-2015":
            if not foodlab and not rule:
                continue
            citation = f"López-Alt, The Food Lab (2015), {ref.get('chapter', '')}, {ref.get('internal_path', '')}, פסקה {ref.get('paragraph_index', 'UNKNOWN')}"
            qualifier = "כלל פרשני" if rule else "טענה מהספר"
            limits = meta.get("exceptions", []) if rule else meta.get("conditions", [])
            explanation += " תנאים: " + " ".join(limits)
            origin = "OBSIDIAN_FOODLAB"
            note = f"{qualifier}; המקור נבדק, ללא אימות מדעי עצמאי."
        else:
            pages = ref.get("printed_pages") or meta.get("printed_page") or "עמודים לא צוינו בהערה"
            citation = f"McGee, On Food and Cooking (2004), {pages}"
            origin = "OBSIDIAN_MCGEE"
            note = "לפי ההערה שבכספת; הסבר מדעי, לא מתכון מלא."
            if mcgee_checked or mcgee_rule:
                limits = meta.get("exceptions", []) if mcgee_rule else meta.get("conditions", [])
                explanation += " תנאים: " + " ".join(limits)
                citation += (
                    f", PDF {ref.get('pdf_pages', 'UNKNOWN')}, עמוד בחלק {ref.get('split_page', 'UNKNOWN')}"
                )
                note = ("כלל פרשני" if mcgee_rule else "טענה מהספר") + "; המקור נבדק, ללא אימות מדעי עצמאי."
        title = node["title_he"][:160]
        if node["id"] in PRACTICAL_TIPS:
            title, explanation = PRACTICAL_TIPS[node["id"]]
        ranked.append(
            (
                score,
                {
                    "title": title,
                    "text": explanation[:1000],
                    "source": citation
                    + " | "
                    + note
                    + " | "
                    + ref.get("split_filename", "")
                    + " | "
                    + node["relative_path"]
                    + " | sha256:"
                    + node["sha256"],
                    "origin": origin,
                    "source_ids": [ref["source_id"], node["id"]],
                    "knowledge_id": node["id"],
                    "revision_sha256": node["sha256"],
                    "usage": "retrieved_background_not_approved_action",
                },
            )
        )
    from app.method_policy import canonical_method
    from app.practical_knowledge import practical_tips

    ranked.extend((100, tip) for tip in practical_tips(query, canonical_method(query))
                  if not query_domains or not food_domains(tip["title"]) or not query_domains.isdisjoint(food_domains(tip["title"])))
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    # Keep both books available when both have relevant evidence.
    selected = []
    for origin in ("OBSIDIAN_SUPPLIED", "OBSIDIAN_MCGEE", "OBSIDIAN_FOODLAB"):
        match = next((tip for _, tip in ranked if tip["origin"] == origin), None)
        if match:
            selected.append(match)
    selected.extend(tip for _, tip in ranked if tip not in selected)
    return selected if limit is None else selected[:limit]


def practical_dish_tips(context, query):
    """Only authored, concrete advice whose ingredients match this dish."""
    text = query.casefold()
    family = context.get("family")
    key, title, advice = None, "", ""
    vegetables = any(
        word in text for word in ("ירקות", "גזר", "תפוח אדמה", "תפוחי אדמה", "vegetables", "carrot", "potato")
    )
    tomato = any(word in text for word in ("עגבני", "tomato"))
    if family in ("vegetables", "soup") and vegetables and tomato:
        key = "EVD-MCG-RNG-CH05-002"
        title = "איך לקבל ירקות רכים ברוטב עגבניות"
        advice = "העגבניות עלולות להאט את ריכוך הירקות הקשים. אם אתה רוצה ירקות רכים ברוטב, אפשר לבשל אותם קודם במים בנפרד. בדוק במזלג חתיכה גדולה: כשהמרכז כמעט רך, סנן והעבר לרוטב להשלמת הבישול. זו אפשרות הכנה למנה, ולא שלב שחייבים להוסיף לכל מתכון."
    elif family in ("meat", "poultry") and any(
        word in text for word in ("מרינדה", "תמלחת", "brining", "marinade")
    ):
        key = "RUL-MEAT-004"
        title = "מה כדאי לעשות לפני הבישול?"
        advice = "אם המטרה היא להוסיף טעם, אפשר להשרות בתיבול המתאים למנה. אם הבשר קשה ואתה מכין תבשיל, ההשריה אינה מחליפה בישול עדין עד לריכוך. לפני המלחה מראש צריך לדעת איזה נתח יש לך ומה משקלו כדי להתאים כמות מלח וזמן השריה."
    elif family in ("meat", "poultry") and any(
        word in text
        for word in (
            "קורקבנ",
            "קורקבן",
            "קוקבנ",
            "קוקבן",
            "כתף",
            "אסאדו",
            "צוואר",
            "gizzard",
            "chuck",
            "shank",
        )
    ):
        key = "EVD-FLB-CH03-003"
        title = "למה ממשיכים לבשל עד שהבשר רך?"
        label = (
            "הקורקבנים"
            if any(word in text for word in ("קורקבנ", "קורקבן", "קוקבנ", "קוקבן", "gizzard"))
            else "הנתח שבחרת"
        )
        advice = f"{label} צריך זמן כדי להתרכך. השחמה מוסיפה צבע וטעם, אבל אינה מחליפה את הריכוך. אם בחרת תבשיל בנוזל, שמור על בעבוע עדין ובדוק חתיכה במזלג: אם היא עדיין קשה ויש נוזל בסיר, המשך ובדוק שוב. בדוק מוכנות בנפרד לפני הגשה."
    elif family in ("meat", "poultry") and any(
        word in text for word in ("חזה", "פילה", "סינטה", "breast", "tenderloin", "sirloin")
    ):
        key = "EVD-FLB-CH03-003"
        title = "איך לשמור על הנתח שלא יתייבש?"
        advice = "הנתח הזה אינו צריך בישול ממושך כדי להתרכך כמו בשר לקדרה. עקוב אחר המרכז במהלך הבישול ובדוק מוכנות לפי סוג הבשר; אל תאריך את החימום רק כדי לקבל עוד צבע מבחוץ."
    if not key:
        return []
    evidence = next((tip for tip in book_tips(query, limit=None) if key in tip["source_ids"]), None)
    if not evidence:
        return []
    return [{**evidence, "title": title, "text": advice, "practical": True}]


def enrich_context(context, query):
    # Family names bridge ingredient aliases (e.g. salmon -> fish) to the notes.
    from app.method_policy import canonical_method
    from app.practical_knowledge import practical_tips

    tips = practical_dish_tips(context, query)
    tips += practical_tips(query, canonical_method(context.get("method", "") or query))
    # Keep every existing tip, especially safety policy. Add only within schema capacity.
    existing = [
        tip for tip in context["tips"] if tip.get("origin") not in ("OBSIDIAN_MCGEE", "OBSIDIAN_FOODLAB", "OBSIDIAN_SUPPLIED")
    ]
    context["tips"] = existing + tips[: max(0, 8 - len(existing))]
    return context
