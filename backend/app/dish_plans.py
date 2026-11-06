"""Scoped authored plans with explicit conditions and reference provenance."""

import hashlib
import re
from functools import lru_cache
from pathlib import Path

import yaml

from app.ingredient_safety import contains, normalize

PREFIX = "CHEF_AUTHORED:guided/"
PLAN_FILE = Path(__file__).with_name("data") / "guided_dish_plans.yaml"


@lru_cache(maxsize=1)
def catalog():
    raw = PLAN_FILE.read_bytes()
    return yaml.safe_load(raw)["plans"], hashlib.sha256(raw).hexdigest()


def active_plan(state):
    for step in state.get("custom_steps", []):
        source = step.get("source", "")
        if source.startswith(PREFIX):
            key = source.removeprefix(PREFIX).split("/")[0]
            plan = catalog()[0].get(key)
            facts = state.get("intake_facts") or {}
            if (
                plan
                and facts.get("family") == plan["family"]
                and {normalize(n) for n in state.get("ingredients", [])}
                == {normalize(n) for n in plan["required"]}
            ):
                return key, plan
    return "", None


def plan_temperature(state, current=None):
    """Targets come from the server catalog, never a round-tripped step value."""
    _, plan = active_plan(state)
    if not plan:
        return None
    targets = [
        detail["minimum_temperature"]
        for detail in plan["steps"]
        if detail.get("minimum_temperature") is not None
        and (current is None or detail["title"] == current["title"])
    ]
    return max(targets) if targets else None


def clear_generated_plan(state):
    """Changing intake must not leave stale recipe quantities or safety checks."""
    removed = {s["id"] for s in state["custom_steps"] if s.get("source", "").startswith(PREFIX)}
    if not removed:
        return
    state["custom_steps"][:] = [s for s in state["custom_steps"] if s["id"] not in removed]
    state["completed_step_ids"] = [value for value in state["completed_step_ids"] if value not in removed]
    state["current_step"] = 0
    state["cooking_memory"].pop("on_heat", None)
    state["timer_deadline"] = state["check_due_at"] = None


def ensure_dish_plan(state):
    if (
        state.get("status") != "active"
        or state["custom_steps"]
        or state.get("safety_hold")
        or state.get("method_warning")
    ):
        return False
    facts = state.get("intake_facts") or {}
    if not facts.get("quantity") or not facts.get("equipment"):
        return False
    if facts.get("family") in {"meat", "fish"} and not facts.get("cut"):
        return False
    scope = " ".join((state["dish_title"], facts.get("cut", ""))).casefold()
    if any(term in scope for term in ("טחון", "ממולא", "קפוא", "minced", "stuffed", "frozen")):
        return False
    names = {normalize(name) for name in state["ingredients"]}
    for key, plan in catalog()[0].items():
        if not any(contains(state["dish_title"], title) for title in plan["titles"]):
            continue
        if facts.get("family") != plan["family"] or facts["equipment"] != plan["equipment"]:
            continue
        if state["method"] not in plan["methods"]:
            continue
        # Do not silently omit additions or turn unknown mixtures into a recipe.
        if names != {normalize(name) for name in plan["required"]}:
            continue
        quantities = {}
        if key == "bread":
            weight = re.fullmatch(r"\s*(\d+)\s*(?:גרם|g)\s*", facts["quantity"], re.IGNORECASE)
            if not weight or not 400 <= int(weight[1]) <= 540:
                continue
            mass = int(weight[1])
            quantities = {
                "dough_g": mass,
                **{
                    label: round(mass * amount / 1612, 1)
                    for label, amount in (("flour_g", 900), ("water_g", 680), ("salt_g", 18), ("yeast_g", 14))
                },
            }
        from app.consultant import user_step

        for index, detail in enumerate(plan["steps"]):
            instruction = detail["instruction"].format(**quantities)
            if index == 0:
                instruction = f"הכמות שביקשת: {facts['quantity']}. " + instruction
            item = user_step(detail["title"], instruction, state["context"])
            item.update(
                source=f"{PREFIX}{key}/v1",
                why=plan["science"],
                successCriteria=[detail["check"]],
                chefQuestions=["בדקת? " + detail["check"]],
                minimum_temperature=detail.get("minimum_temperature"),
            )
            state["custom_steps"].append(item)
        state["current_step"] = 0
        state["completed_step_ids"] = []
        targets = [
            s["minimum_temperature"]
            for s in state["custom_steps"]
            if s.get("minimum_temperature") is not None
        ]
        state["context"]["minimum_temperature"] = max(targets) if targets else None
        state["context"]["minimum_rest_seconds"] = 0
        state["decision_questions"] = []
        state["guidance_links"] = [{"title": "מקור לתוכנית — " + key, "url": url} for url in plan["sources"]]
        return True
    return False


def completion_warning(state, current):
    key, plan = active_plan(state)
    if not plan or not current or not current.get("source", "").startswith(PREFIX):
        return None
    minimum = plan_temperature(state, current)
    if minimum is not None and (
        state.get("measured_temperature") is None or state["measured_temperature"] < minimum
    ):
        return f"אל תעבור להגשה: דווח מדידה בחלקים העבים של לפחות {minimum:g}°C. " + current["instruction"]
    if key in {"beef", "fish"}:
        cooking = next((s for s in state["custom_steps"] if plan_temperature(state, s) is not None), None)
        if cooking is None:
            return "שלב בדיקת הבישול הוסר או נערך. יש להשלים בדיקת מוכנות ומדידה לפני הגשה."
        if (
            current["id"] != cooking["id"]
            and state["current_step"] > state["custom_steps"].index(cooking)
            and cooking["id"] not in state["completed_step_ids"]
        ):
            return "טרם אישרת את בדיקת הבישול והמדידה. חזור לשלב הבישול ובדוק לפני הגשה."
    return None


def plan_reply(state, text):
    key, plan = active_plan(state)
    if not plan:
        return None
    steps = state["custom_steps"]
    current = steps[state["current_step"]]
    if "חזור לבישול" in text or "מה דיווחתי" in text:
        memory = state.get("cooking_memory", {})
        reports = " ".join(
            memory.get(field, "") for field in ("reported_problem", "missing_ingredient_report", "on_heat")
        )
        return f"אתה מכין {state['dish_title']}. דיווחיך: {reports} הפעולה הנוכחית: {current['instruction']}"
    if "שליקה" in text:
        return (
            "שליקה היא בישול בנוזל חם ללא רתיחה חזקה. זו שאלה צדדית; המנה והשלב נשמרו. "
            + current["instruction"]
        )
    if text.lstrip().startswith("למה"):
        return plan["science"]
    if "אין לי" in text:
        if key == "beef" and "ציר" in text:
            return "אפשר להשתמש במים עד כיסוי הבשר, כפי שמתואר בתוכנית. הטעם יהיה עדין יותר; תקן מלח רק בסוף, אחרי שהבשר מבושל."
        if key == "fish" and "לימון" in text:
            return "אפשר להגיש בלי לימון. אם יש חומץ, נסה טיפה על ביס מהדג המבושל; אל תשפוך כמות על כל הדג. זמן האפייה ובדיקת המדחום אינם משתנים."
        if key == "legumes" and "עגבניות" in text:
            return "אפשר לוותר על העגבניות. בשל את העדשים במים לפי התוכנית וחבר לירקות הרכים. התאם בסוף מלח בטעימה; אין צורך להאריך זמן בגלל החוסר."
        if key == "soup" and "בצל" in text:
            return "אפשר בלי בצל. אם משתמשים בכרישה, פצל לאורך, שטוף היטב בין השכבות וחתוך דק. רכך אותה במקום הבצל עד שהיא רכה; אין צורך להוסיף את שניהם."
        if key == "bread" and "שמרים" in text:
            return "לפני החלפה: האם אלה שמרים טריים, יבשים פעילים או שמרי אינסטנט? אל תחליף בכמות שווה בלי לזהות את הסוג; בדוק את הוראות האריזה ודווח מה כתוב."
        return "אל תוסיף תחליף לא מזוהה. כתוב איזה רכיב חסר ומה יש במקום; אלרגיות ושיטת הבישול נשארות בתוקף."
    if any(term in text for term in ("נשרף", "שחור")):
        return "הורד את הסיר מהחום. אל תגרד ואל תערבב את התחתית השרופה; העבר רק חלק שאינו שרוף לסיר נקי, בלי לטעום בשר שטרם בושל. דווח מה נשרף לפני המשך."
    if key == "beef" and "קשה" in text:
        return "בדוק שיש נוזל שמכסה את הבשר. הוסף מים חמים אם חסר והמשך בבעבוע עדין, לא ברתיחה חזקה. בדוק שוב במזלג בעוד כ־20 דקות; זו תזכורת לבדיקה, לא זמן סיום מובטח."
    if key == "fish" and any(term in text for term in ("יבש", "מתפרק")):
        return "מדוד כעת במרכז החלק העבה. אם עדיין פחות מ־63°C, המשך אפייה ובדוק שוב; אין להגיש לפי מראה בלבד. אם הושג היעד, הוצא מהתנור. אי אפשר להחזיר עסיסיות שאבדה; הגש בעדינות עם מעט שמן או נוזל מהרוטב."
    if key == "legumes" and any(term in text for term in ("קשות", "קשה")):
        return "השאר את העגבניות בצד. בדוק שהעדשים מכוסות במים והמשך בבעבוע עדין. צנן כמה בכפית ובדוק שוב עד שהמרכז רך. גיל העדשים עשוי להאריך את הבישול."
    if key == "soup" and any(term in text for term in ("דליל", "מימי")):
        return "בדוק קודם שתפוח האדמה רך. מעך כמה קוביות מבושלות וערבב במרק. עדיין דליל? בשל בלי מכסה וערבב עד הסמיכות הרצויה; טעם מלח רק אחרי ההסמכה."
    if key == "soup" and "מלוח" in text:
        return "אל תוסיף מלח ואל תבשל בלי מכסה כדי להסמיך; זה ירכז את המליחות. הוסף מעט מים חמים והמשך בבעבוע עד שתפוח האדמה רך. טעם כפית לאחר צינון וחזור על דילול קטן רק אם צריך. תפוח האדמה אינו מוציא את המלח מהמרק."
    if key == "bread" and "לא תפח" in text:
        return "כסה והשאר במקום נעים ללא חימום ישיר; בחדר קר יידרש יותר זמן. בדוק אם יש בועות והתרחבות. אם אין פעילות כלל, דווח על סוג השמרים ותוקפם ועל טמפרטורת המים; אל תאפה בצק צפוף כאילו תפח."
    if any(term in text for term in ("למה", "מדע")):
        return plan["science"]
    if any(term in text for term in ("לשמור", "להגיש", "אחסון", "הגשה", "מוכנה", "מה למדתי")):
        check = next((s for s in steps if s.get("minimum_temperature") is not None), None)
        readiness = ("לפני הגשה, בדוק: " + check["successCriteria"][0] + ". ") if check else ""
        return readiness + steps[-1]["instruction"]
    return current["instruction"] + " בדוק: " + current["successCriteria"][0] + "."
