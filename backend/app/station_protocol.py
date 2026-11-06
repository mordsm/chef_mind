"""One deterministic station contract for both guidance surfaces, including gaps.

Editorial process proposals remain separate from approved claim citations. Unknown
temperatures/times are explicit gaps; safety holds always override cooking advice.
"""

import re
from pathlib import Path

import yaml

SOURCE = Path(__file__).with_name("data") / "station_profiles.yaml"
TITLES = [
    "פקודת תחנה ו-Mise en place",
    "ביצוע — מעלות, זמן וסימן חושי",
    "המדע של אותו צעד",
    "איזון טעם, מרקם והתאמת משקה",
    "Wikilinks ותגיות",
    "מה כבר ידוע ומה עדיין חסר",
]


def configuration():
    from culinary_engine.src.validator import parse

    return parse(SOURCE.read_text(encoding="utf-8"))


def identify(title, family="", config=None):
    config = config or configuration()
    from app.knowledge_graph import phrase_spans

    profile = next((p for p in config["profiles"] if phrase_spans(title.casefold(), p["aliases"])), None)
    if profile:
        return profile, profile["family"]
    if not family or family in {"general", "other"}:
        from app.culinary_engine_api import configuration as engine_configuration

        registry = engine_configuration().registry_data["ingredients"]
        for key, ingredient in registry.items():
            if phrase_spans(title.casefold(), [ingredient["name"].casefold(), key.replace("_", " ")]):
                family = config.get("archetype_families", {}).get(ingredient["archetype"], family)
                break
    return None, {
        "poultry": "meat",
        "beef": "meat",
        "pasta": "starch",
        "rice": "starch",
        "grains": "starch",
        "vegetable": "vegetables",
    }.get(family, family)


def render_text(protocol):
    text = "\n\n".join(
        f"{i}. {block['title']}\n{block['text']}" for i, block in enumerate(protocol["blocks"], 1)
    )
    if protocol.get("current_action"):
        text = "עכשיו: " + protocol["current_action"]["text"] + "\n\n" + text
    if protocol["next_question"]:
        text += "\n\nהפרט הבא לביצוע: " + protocol["next_question"]
    return text


def obsidian_note(protocol, title):
    frontmatter = {
        "type": "culinary-station-log",
        "title": title,
        "links": protocol["wikilinks"],
        "tags": protocol["tags"],
        "knowledge_gap_flagged": protocol["knowledge_gap_flagged"],
        "recommended_reading": protocol["recommended_reading"],
        "source_ids": protocol["source_ids"],
        "editorial_references": protocol.get("editorial_references", []),
        "action_citations": protocol.get("action_citations", []),
        "unverified": protocol["gaps"],
    }
    return (
        "---\n"
        + yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False)
        + "---\n\n"
        + render_text(protocol)
        + "\n"
    )


def build_protocol(
    title,
    *,
    family="",
    facts=None,
    current=None,
    advice="",
    blocked=False,
    gaps=(),
    model_status="rules_only",
    allergies=(),
    method_warning="",
    method="",
    ingredients=(),
    user_message="",
):
    cfg = configuration()
    from app.food_hazards import red_bean_warning
    hazard = red_bean_warning([title, *ingredients], user_message)
    if hazard:
        advice = (advice + "\n" if blocked and advice else "") + hazard["text"]
        blocked = True
    profile, family = identify(title, family, cfg)
    facts = facts or {}
    name = title or "המנה"
    reading = cfg["readings"].get(family, cfg["readings"]["general"])
    unknowns = list(gaps)
    if profile is None:
        unknowns.append("אין פרופיל תחנה ייעודי מאומת ל־" + name + "; ההכוונה היא לפי המשפחה בלבד.")
    if model_status in {"unavailable", "disabled"}:
        unknowns.append("זיהוי המודל אינו זמין; הפרוטוקול נבנה מקומית משם המנה והמשפחה.")
    if profile:
        unknowns.extend(profile["gaps"])
    if facts.get("family") and profile and facts["family"] != profile["family"]:
        blocked = True
        advice = "שם המנה והמשפחה שדווחה סותרים זה את זה; אמת את חומר הגלם לפני חימום."
        unknowns.append("סתירה בין זיהוי מקומי לבין המשפחה שנבחרה.")
    if family == "fish" and {str(a).strip().casefold() for a in allergies} & {"fish", "דג", "דגים"}:
        blocked = True
        advice = "דג סותר אלרגיה שדווחה. אל תכין ואל תגיש את המנה."
    preparation = (profile or {}).get(
        "preparation",
        f"סו־שף, סדר תחנה עבור {name}: משטח נקי, כלי עבודה, כלי הגשה וחומרי גלם מדודים. הפרד נא ממוכן. התחל בהכנות בלבד עד לאימות הטיפול המתאים.",
    )
    science = (profile or {}).get(
        "science",
        {
            "fish": "קולגן דגים רגיש לחום וסיבי השריר מתכווצים; חימום אגרסיבי עלול לפרק את הנתח ולייבשו. הסבר משפחתי, לא בדיקה של הדג המסוים.",
            "meat": "חלבוני השריר מתכווצים בחימום; כמות רקמת החיבור משפיעה על הזמן לריכוך. אין להסיק יעד בישול משם המשפחה בלבד.",
            "eggs": "חימום משנה את מבנה חלבוני הביצה ויוצר רשת קרישה; רשת הדוקה מדי עלולה להפריש מים.",
            "starch": "עמילן קולט מים ומשנה את מבנהו בחימום; סוג המוצר קובע את קצב הריכוך.",
            "vegetables": "חום ורמת החומציות משפיעים על דפנות התאים והמרקם; גודל החיתוך משפיע על אחידות החימום.",
        }.get(family, "המנגנון המדעי הספציפי טרם אומת במאגר; אל תייחס לחומר הגלם תכונות שלא זוהו."),
    )
    flavor = (profile or {}).get(
        "flavor",
        "טעם רכיב שכבר מוכן לאכילה בכפית נקייה. חסר מלח? הוסף קמצוץ קטן, ערבב וטעם שוב. רוצה טעם לימוני? נסה כמה טיפות לימון בכף נפרדת לפני שמוסיפים לסיר. אפשר לשתות מים לצד המנה.",
    )
    if family == "fish" and not profile:
        flavor += " הצעת התאמה, לא כלל מאומת למנה: Chenin Blanc יבש מ־Anjou, עמק הלואר, צרפת."
    execution = "עדיין חסרה כאן הוראת בישול מתאימה למנה ולשיטה. אל תתחיל לחמם לפי ניחוש. השלם את פרטי המנה או בחר מתכון נתמך כדי לקבל את הפעולה הבאה."
    if current and current.get("instruction"):
        preparation += " הפעולה שנבחרה: " + current["title"] + "."
        execution = (
            current["instruction"]
            + " זמן וטמפרטורה שלא צוינו במקור: UNKNOWN; אין להשלים מספרים. סימן לבדיקה: "
            + "; ".join(current.get("successCriteria", []))
        )
        if current.get("source") == "CHEF_AUTHORED:salad_pilot_v1":
            execution = "זהו מסלול להכנה קרה, ללא חימום. המשך לפי הפעולה הנוכחית וסמן אישור ביצוע רק אחרי שבדקת: " + "; ".join(current.get("successCriteria", []))
    links = (profile or {}).get(
        "wikilinks",
        ["[[Culinary Station]]", "[[" + ("Fish Collagen" if family == "fish" else "Heat Transfer") + "]]"],
    )
    tags = (profile or {}).get(
        "tags",
        [
            "culinary/knowledge-gap",
            "culinary/family/"
            + (
                family
                if family in cfg["readings"] or family in {"starch", "vegetables", "legumes", "soup"}
                else "unknown"
            ),
        ],
    )
    if family == "fish":
        safety = cfg["fish_safety"]
        preparation += " שמור את הדג מתחת ל־4°C בזמן ההכנות."
        if safety["approval_status"] == "APPROVED":
            execution = (
                "לנתח שאינו טחון או ממולא: בשל בעדינות בתוך רוטב חם. בשיטה הזו לא מרתיחים את הרוטב.\n"
                "1. חמם את הרוטב ומדוד אותו במדחום: 70–80°C הם חום הרוטב בסיר, ולא מספר בכפתור הכיריים. הנמך או הגבר את האש כדי לשמור על הטווח הזה גם אחרי הכנסת הדג.\n"
                f"2. הכנס מדחום מהצד עד מרכז החלק העבה של כל נתח, בלי לגעת בסיר או בעצם. המשך לבשל עד שהמרכז מגיע ל־{safety['core_c']}°C. "
                f"רק אז ספור {safety['hold_seconds']} שניות לפחות, כשהמרכז נשאר בחום הזה או מעליו. זה אינו זמן הבישול הכולל.\n"
                "3. " + cfg["fish_time_guide"]["text"] + "\n"
                "4. לבדיקה נוספת, פתח מעט את מרכז הנתח במזלג: הבשר צריך להיפרד בקלות לשכבות וכבר לא להיראות שקוף. המראה עוזר לבדוק מרקם; את יעד החום בודקים במדחום.\n"
                + safety["rest"]
                + " "
                + safety["cooling"]
            )
        else:
            execution = "יעד הליבה ממתין לאישור בעל המערכת. אל תחמם עדיין; שמור מתחת ל־4°C. זמן חימום: UNKNOWN. בדוק נתח ועובי; סימן חושי אינו אישור בטיחות."
            unknowns.append("יעד הליבה לדגים טרם אושר; אין פרוטוקול חימום מאושר.")
        unknowns.append("פרוטוקול משפחתי לדג שלם ולא ממולא; תהליך HACCP למטבח המסוים לא אומת.")
        from app.method_policy import canonical_method

        selected = canonical_method(method) if method else None
        if selected and selected != "boil_simmer":
            execution = f"השיטה שבחרת ({method}) נשמרה. אין בפרופיל התחנה תהליך מאומת עבורה; בצע הכנות קרות בלבד מתחת ל־4°C. טמפרטורת חימום ומשך: UNKNOWN. אל תחליף שיטה ללא בחירה מפורשת."
            unknowns.append("הפרוטוקול המפורט הוא לשליקה ברוטב בלבד, לא לשיטה שנבחרה.")
        scope = " ".join([title, facts.get("cut", "")]).casefold()
        if any(term in scope for term in ("טחון", "ממולא", "minced", "stuffed", "קפוא", "frozen")):
            execution = "הפרוטוקול אינו מתאים לדג טחון, ממולא או קפוא. אל תבצע חימום לפי פרופיל הנתח השלם; שמור מתחת ל־4°C ובחר תהליך ייעודי מאומת. טמפרטורה ומשך: UNKNOWN."
            unknowns.append("מצב הדג או מבנהו מחייבים תהליך בטיחות ייעודי.")
    if allergies:
        preparation = (
            f"בדוק קודם התאמת כל רכיב לאלרגיות שדווחו: {', '.join(allergies)}. אל תשתמש בחלב, בציפוי או בתוספת בלי בדיקה. "
            + preparation
        )
    if blocked or method_warning:
        preparation = "עצור חימום והגשה. " + (advice or method_warning or "טפל בסיכון שדווח לפני המשך.")
        execution = "אל תבצע את פרוטוקול החימום כל עוד החסימה קיימת. נדרשים בירור ותנאי בטיחות מאומתים; זמן וטמפרטורה להמשך: UNKNOWN."
        unknowns.append("קיימת חסימת בטיחות או שיטה שאינה מאושרת.")
        flavor = (
            "אל תטעם ואל תגיש כל עוד קיימת חסימת בטיחות. התאמת טעם, מרקם ומשקה תיעשה רק לאחר בירור הסיכון."
        )
    question = ""
    if not family or family in {"general", "other"}:
        question = f"מה חומר הגלם המרכזי או המשפחה של {name}?"
    elif family in {"fish", "meat"} and not facts.get("cut"):
        question = f"איזה נתח של {name} יש לך ומה עוביו בס״מ?"
    elif not facts.get("quantity"):
        question = f"מה הכמות של {name}?"
    pages = reading['pages'] if reading['pages'] != 'UNKNOWN' else 'מספרי העמודים עדיין לא נבדקו'
    reading_text = f"{reading['author']}, {reading['book']}, {reading['edition']}, פרק {reading['chapter']}, עמודים {pages}."
    gap_text = (
        "Knowledge Base Extension Needed — סימון פנימי שפירושו: צריך להשלים מידע מעשי במאגר. "
        "אין פירושו שהספר חסר.\n"
        + reading_text
        + "\nהספר מסביר עקרונות בישול. ההפניה אליו אינה אומרת שכל הוראה למנה שלך נבדקה בו. "
        "תנאי הבטיחות במטבח שלך לא נבדקו במסגרת ההנחיה הזו."
    )
    if family == "fish":
        gap_text += (
            "\nבהכנה הזו אין צורך להשרות את הדג. מייבשים אותו ומבשלים ברוטב. "
            "אם רוצים טעם לימוני, מוסיפים מעט לימון לרוטב וטועמים."
            "\n2-MIB הוא שם של חומר שיכול לגרום לריח אדמתי בחלק מהדגים. "
            "לא בדקנו שהוא נמצא בדג שלך, ואין לנו בסיס לומר שהשריה ביתית מפרקת אותו. "
            "אין להשתמש בהשריה כדי להסתיר ריח של קלקול."
            "\nHACCP הוא תהליך מסודר למניעת סכנות במזון: בודקים היכן עלולה להתרחש בעיה, "
            "מגדירים מה צריך למדוד ומתעדים את הבדיקה. הכוונה כאן היא שלא נערכה ביקורת על "
            "הציוד, הקירור ושגרת העבודה במטבח שלך; אין בכך פעולה נוספת שעליך לנחש."
        )
    blocks = [
        {"title": label, "text": text}
        for label, text in zip(
            TITLES,
            [
                preparation,
                execution,
                science,
                flavor,
                " ".join(links + ["#" + tag for tag in tags]),
                gap_text,
            ],
            strict=True,
        )
    ]
    gap_summary = (
        "הספר מספק הסבר כללי על הבישול, אבל אין כאן מתכון בדוק לכל נתח ועובי. "
        "לכן איני נותן זמן בישול מדויק כשאין לי בסיס לכך. "
        "כדי להתאים את ההנחיה, השלם את הפרט הבא שמופיע למטה."
    )
    if family == "fish":
        gap_summary = (
            "יש במאגר חומר על דגים מתוך הספר של הרולד מקגי. הוספנו גם זמני בישול משוערים לפי עובי. "
            "כדי להתאים אותם אליך צריך לדעת מה עובי הנתח; הזמן בפועל יכול להשתנות. "
            "בהכנה הזו אין צורך להשרות את הדג לפני הבישול. "
            "ההפניה לספר היא לרקע ולהעמקה; אין צורך להוסיף אותו שוב למאגר."
        )
    blocks[5]["display_text"] = gap_summary
    blocks[5]["details_text"] = gap_text
    blocks[5]["text"] = gap_summary + "\n" + gap_text
    if reading.get("resources"):
        blocks[5]["resources"] = reading["resources"]
    if hazard:
        question = hazard["question"]
        blocks[5]["resources"] = [*blocks[5].get("resources", []), {
            "title": "FDA — הכנה בטוחה של שעועית יבשה", "url": hazard["source"],
            "scope": "הסבר על הסיכון בשעועית שלא בושלה כראוי ועל ההכנה הנדרשת.",
        }]
    protocol = {
        "version": 1,
        "profile_id": (profile or {}).get("id"),
        "family": family,
        "blocks": blocks,
        "next_question": question,
        "knowledge_gap_flagged": True,
        "recommended_reading": reading,
        "wikilinks": links,
        "tags": tags,
        "gaps": list(dict.fromkeys(unknowns)),
        "source_ids": (profile or {}).get("sources", ["SRC-MCGEE-2004"]),
        "provenance": "EDITORIAL_FAMILY_PROTOCOL_NOT_SPECIES_VALIDATION",
    }
    if family == "fish":
        protocol["source_ids"] = list(dict.fromkeys([
            *protocol["source_ids"], "SRC-FDA-SEAFOOD-CONSUMER", cfg["fish_time_guide"]["source_id"]
        ]))
    if hazard:
        protocol["source_ids"].append(hazard["source_id"])
    protocol["source_ids_semantics"] = "reference_index_not_proof_of_claim_support"
    protocol["editorial_references"] = [{"source_id": value, "usage": "editorial_reference"} for value in protocol["source_ids"]]
    protocol["action_citations"] = []
    if blocked or method_warning:
        protocol["current_action"] = {"text": preparation if blocked else execution, "kind": "safety"}
    elif current and current.get("instruction"):
        protocol["current_action"] = {"text": current["instruction"], "kind": "action"}
    if current and current.get("source") == "CHEF_AUTHORED:salad_pilot_v1":
        from app.cooking_pilot import PRODUCE_SOURCE, PILOT_SOURCE
        for value in (PILOT_SOURCE, PRODUCE_SOURCE):
            protocol["source_ids"].append(value)
            protocol["editorial_references"].append({"source_id": value, "usage": "editorial_pilot_and_safety_reference"})
    protocol["text"] = render_text(protocol)
    protocol["obsidian_markdown"] = obsidian_note(protocol, name)
    return protocol


def attach_station(state):
    steps = state.get("custom_steps", [])
    current = steps[state.get("current_step", 0)] if 0 <= state.get("current_step", 0) < len(steps) else None
    info = state.get("intake_guidance", {})
    advice = next((m["text"] for m in reversed(state.get("messages", [])) if m["role"] == "chef"), "")
    protocol = build_protocol(
        state["dish_title"],
        family=info.get("family") or (state.get("context") or {}).get("family", ""),
        facts=state.get("intake_facts"),
        current=current,
        advice=advice,
        blocked=state.get("safety_hold", False),
        method_warning=state.get("method_warning", ""),
        model_status=state.get("dish_identity", {}).get("status", "rules_only"),
        allergies=state.get("allergies", []),
        method=state.get("method", ""),
        ingredients=state.get("ingredients", []),
        user_message=next((m["text"] for m in reversed(state.get("messages", [])) if m["role"] == "user"), ""),
    )
    focus = state.get("learning_focus") or {}
    explanation = focus.get("text", "")
    if explanation and not state.get("safety_hold") and not state.get("method_warning"):
        # Keep the contextual answer, but do not import legacy fish temperature
        # advice or repeat its interview questions ahead of the one next detail.
        sentences = re.split(r"(?<=[.!?])\s+|\n+", explanation)
        useful = [s for s in sentences if s and "Knowledge Base Extension Needed" not in s]
        if protocol["family"] == "fish":
            useful = [s for s in useful if not re.search(r"\d.*(?:°|מעלות|דקות|שניות|minutes|seconds)", s)]
        if useful:
            # The actual answer belongs in the foreground, not inside closed science.
            answer = " ".join(useful)[:1200]
            if protocol.get("current_action", {}).get("kind") != "safety":
                protocol["current_action"] = {
                    "text": answer,
                    "kind": "warning" if any(word in answer for word in ("שרוף", "חריכה", "עצור", "סיכון")) else "answer",
                }
            protocol["source_ids"] = list(
                dict.fromkeys([*protocol["source_ids"], *focus.get("source_ids", [])])
            )
            protocol["text"] = render_text(protocol)
            protocol["obsidian_markdown"] = obsidian_note(protocol, state["dish_title"])
    state["station_protocol"] = protocol
    if info:
        info["guidance"] = protocol["text"]
    return protocol
