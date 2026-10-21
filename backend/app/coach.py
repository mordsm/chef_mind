"""Cooking-coach workflow. State changes require reported observations, never elapsed time.

Starter recipes are authored instructional examples, not professionally kitchen-tested recipes.
Timing is an advisory check-in interval. Food safety follows the cited government guidance.
"""

from copy import deepcopy
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import Depends
from pydantic import Field
from sqlalchemy import select

from app.culinary_context import ContextTip, DishContext
from app.db import CookingRecord
from app.decision_table import DecisionQuestion
from app.knowledge import DomainError, audit
from app.knowledge_graph import audit_graph, graph
from app.schemas import StrictModel

SAFETY = "https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures"
TECHNIQUE = "https://www.ciachef.edu/blog/3-types-cooking-methods-foods-love/"


class ChefOption(StrictModel):
    id: str = Field(max_length=50)
    label: str = Field(max_length=120)
    result: str = Field(pattern="^(pass|wait|recover)$")
    response: str = Field(max_length=600)


class CoachMessage(StrictModel):
    role: str = Field(pattern="^(chef|user)$")
    text: str = Field(max_length=4000)


class SmartStep(StrictModel):
    id: str = Field(default="", max_length=80)
    title: str = Field(max_length=160)
    instruction: str = Field(max_length=1000)
    why: str = Field(max_length=1000)
    commonMistakes: list[str] = Field(max_length=10)
    successCriteria: list[str] = Field(min_length=1, max_length=10)
    recoveryActions: list[str] = Field(min_length=1, max_length=10)
    chefQuestions: list[str] = Field(min_length=1, max_length=10)
    possibleFailures: list[str] = Field(min_length=1, max_length=10)
    recoveryInstructions: list[str] = Field(min_length=1, max_length=10)
    options: list[ChefOption] = Field(min_length=1, max_length=8)
    check_after_seconds: int = Field(ge=0, le=14400)
    estimated_seconds: int = Field(ge=0, le=14400)
    minimum_temperature: float | None = None
    source: str = TECHNIQUE
    next_step_prep: str = Field(default="", max_length=1000)


def step(
    title,
    instruction,
    why,
    criteria,
    question,
    seconds=0,
    failure="התוצאה עדיין אינה מתאימה",
    recovery="עצור ובדוק את המצב לפני המשך.",
    options=None,
    temperature=None,
):
    options = options or [
        ChefOption(
            id="ready",
            label="כן, בדקתי וזה המצב",
            result="pass",
            response="הבדיקה נרשמה. אפשר לסיים את השלב.",
        ),
        ChefOption(
            id="not-yet",
            label="עדיין לא",
            result="wait",
            response="נשארים בשלב הנוכחי; בדוק שוב כשהמצב משתנה.",
        ),
    ]
    return SmartStep(
        title=title,
        instruction=instruction,
        why=why,
        commonMistakes=[failure],
        successCriteria=[criteria],
        recoveryActions=[recovery],
        chefQuestions=[question],
        possibleFailures=[failure],
        recoveryInstructions=[recovery],
        options=options,
        check_after_seconds=seconds,
        estimated_seconds=seconds,
        minimum_temperature=temperature,
        source=SAFETY if temperature else TECHNIQUE,
    ).model_dump()


ONION = step(
    "טיגון הבצל",
    "טגן את הבצל בחום מתון וערבב מדי פעם; בדוק רכות וצבע.",
    "למנה הזאת נרצה בצל רך וזהוב לפיתוח טעם; מידת ההשחמה משתנה בין מנות.",
    "הבצל רך וזהוב, ללא חלקים שרופים",
    "מה מצב הבצל?",
    240,
    "חום גבוה מדי או השחמה לפני שהבצל מתרכך",
    "הפחת חום. אם הבצל שחור ובעל טעם שרוף, הסר אותו והתחל מחדש.",
    [
        ChefOption(
            id="white",
            label="לבן",
            result="wait",
            response="לפי הדיווח הבצל עדיין בהיר. המשך בחום מתון ובדוק רכות וצבע.",
        ),
        ChefOption(
            id="clear",
            label="שקוף",
            result="wait",
            response="הבצל התרכך בחלקו. למנה הזאת המתן להזהבה קלה, תוך בדיקה שלא נשרף.",
        ),
        ChefOption(
            id="golden",
            label="רך וזהוב",
            result="pass",
            response="לפי הדיווח הושג המרקם הרצוי. אפשר לסיים את השלב.",
        ),
        ChefOption(
            id="dark",
            label="כהה מדי / שרוף",
            result="recover",
            response="הפחת את החום. אם יש חלקים שחורים וריח שרוף, הסר אותם; טעם שרוף אינו מתוקן בהוספת מים.",
        ),
    ],
)

RECIPES = {
    "shakshuka": {
        "id": "shakshuka",
        "title": "שקשוקה ביתית",
        "icon": "🍳",
        "allergens": ["eggs"],
        "ingredients": ["בצל", "עגבנייה", "ביצה", "שמן זית"],
        "steps": [
            step(
                "הכנת חומרי הגלם",
                "הכן בצל קצוץ, עגבניות חתוכות, ביצים, שמן ותבלינים לפי מספר הסועדים.",
                "הכנה מוקדמת מאפשרת להתרכז במחבת.",
                "המרכיבים והכלים מוכנים",
                "האם חומרי הגלם והכלים מוכנים?",
                failure="תחילת חימום לפני שהחיתוך הסתיים",
                recovery="כבה את החימום והשלם את ההכנות.",
            ),
            ONION,
            step(
                "בישול העגבניות",
                "הוסף את העגבניות ותבל לפי הטעם. בשל בבעבוע עדין וערבב מדי פעם.",
                "התרככות וריכוז הרוטב יוצרים בסיס לביצים.",
                "העגבניות רכות והרוטב סמיך אך אינו יבש",
                "האם הרוטב רך וסמיך מספיק?",
                300,
                "רוטב יבש מדי או נוזלי מדי",
                "אם הרוטב יבש הוסף מעט מים; אם הוא דליל המשך בישול עדין ללא מכסה ובדוק שוב.",
            ),
            step(
                "הוספת ביצים",
                "צור גומות, הוסף ביצים ובשל עד שהחלבון והחלמון יציבים. בדוק בפועל; הטיימר אינו קובע מוכנות.",
                "בישול הביצים דורש בדיקה נפרדת ממרקם הרוטב.",
                "החלבון והחלמון יציבים",
                "האם גם החלבון וגם החלמון יציבים?",
                180,
                "הגשה כשהביצה עדיין נוזלית",
                "המשך בישול עד שהחלבון והחלמון יציבים.",
            ),
        ],
    },
    "pasta": {
        "id": "pasta",
        "title": "פסטה ברוטב עגבניות",
        "icon": "🍝",
        "allergens": ["wheat"],
        "ingredients": ["פסטה", "עגבנייה", "שמן זית"],
        "steps": [
            step(
                "הכנה",
                "הכן פסטה, עגבניות, שמן, מים וסיר; בדוק את הוראות האריזה ואת האלרגנים.",
                "האריזה מגדירה את זמן הבישול לסוג הפסטה שלך.",
                "המרכיבים והוראות האריזה מוכנים",
                "האם בדקת את האריזה והכנת את המרכיבים?",
            ),
            step(
                "הכנת הרוטב",
                "בשל את העגבניות במעט שמן עד שהן מתרככות, וערבב מדי פעם.",
                "בישול עדין מרכז את הרוטב.",
                "הרוטב רך ואינו חרוך",
                "האם הרוטב רך וללא חלקים חרוכים?",
                240,
                "רוטב נדבק לתחתית",
                "הפחת חום והוסף מעט מים אם חסר נוזל; אל תגרד חלקים שרופים לתוך הרוטב.",
            ),
            step(
                "בישול הפסטה",
                "בשל במים לפי הוראות האריזה. בדוק מרקם לקראת סיום; שמור מעט ממי הבישול לפני הסינון.",
                "סוג הפסטה ועובייה משפיעים על זמן ההכנה.",
                "הפסטה במרקם הרצוי לפי בדיקה",
                "האם הפסטה במרקם הרצוי?",
                240,
                "הסתמכות על טיימר בלי בדיקת מרקם",
                "אם היא קשה המשך לפי הוראות האריזה ובדוק שוב; אם רכה מדי סנן מיד.",
            ),
            step(
                "חיבור והגשה",
                "ערבב את הפסטה והרוטב; הוסף מעט ממי הבישול אם צריך לדלל.",
                "נוזל נוסף מאפשר להתאים את סמיכות הרוטב.",
                "הרוטב מצפה את הפסטה והטעם נבדק",
                "האם הסמיכות והטעם מתאימים?",
                failure="הוספת יותר מדי נוזל בבת אחת",
                recovery="הוסף נוזל בהדרגה; אם דליל, ערבב מעט על חום מתון ובדוק שוב.",
            ),
        ],
    },
    "chicken": {
        "id": "chicken",
        "title": "עוף בתנור",
        "icon": "🍗",
        "allergens": [],
        "ingredients": ["עוף", "שמן זית"],
        "steps": [
            step(
                "הכנה",
                "בחר מתכון מתאים לנתח ולמשקל. הכן תבנית, תיבול ומדחום; השתמש בהגדרת התנור שבמתכון.",
                "הזמן תלוי בנתח, במשקל ובתנור. אין כאן זמן צלייה אחיד לכל עוף.",
                "יש מתכון מתאים, כלים ומדחום",
                "האם יש לך מתכון מתאים ומדחום?",
                failure="בחירת זמן אחיד בלי לזהות את הנתח",
                recovery="עצור ובחר מתכון שמתאים לנתח ולמשקל לפני ההכנה.",
            ),
            step(
                "תיבול וסידור",
                "תבל לפי המתכון וסדר בתבנית. הפרד כלים שנגעו בעוף נא ממזון מוכן.",
                "הפרדת הכלים מפחיתה מגע בין עוף נא למזון מוכן.",
                "התבנית מוכנה והכלים הופרדו",
                "האם התבנית מוכנה והכלים הנקיים מופרדים?",
                failure="שימוש בכלי שנגע בעוף נא להגשה",
                recovery="החלף לכלי נקי ושטוף ידיים ומשטחים שבאו במגע עם העוף הנא.",
            ),
            step(
                "צלייה ובדיקת טמפרטורה",
                "צלה לפי המתכון. מדוד בעובי הנתח בלי לגעת בעצם; נדרשים לפחות 74°C. בדוק יותר ממקום אחד כשיש כמה נתחים.",
                "צבע וזמן אינם מחליפים מדידת טמפרטורה בעוף.",
                "נמדדו לפחות 74°C בחלקים העבים",
                "מה הטמפרטורה הנמוכה ביותר שמדדת בחלקים העבים?",
                600,
                "הסתמכות על צבע או על זמן בלבד",
                "אם המדידה נמוכה מ־74°C, המשך לצלות ובדוק שוב. ללא מדחום אין אישור מוכנות מהמערכת.",
                temperature=74,
            ),
            step(
                "הגשה בכלים נקיים",
                "העבר לכלי נקי בעזרת כלי הגשה נקיים.",
                "כלי שנגע בעוף נא אינו מתאים להגשת העוף המבושל ללא ניקוי.",
                "כלי ההגשה נקיים",
                "האם כלי ההגשה נקיים ולא נגעו בעוף נא?",
                failure="החזרה לכלי שבו היה העוף הנא",
                recovery="השתמש בכלי נקי; אם נוצר מגע עם עוף נא, עצור וברר את הטיפול המתאים.",
            ),
        ],
    },
}
RECIPES["shakshuka"]["steps"][-1]["source"] = SAFETY


class CoachCommand(StrictModel):
    action: str = Field(
        pattern="^(start|start_custom|answer|complete|problem|pause|resume|check_in|personality|timer|timer_cancel|ask|report|finish|add_step|edit_step|remove_step|select_step|move_step|mode|update_plan|adopt_path)$"
    )
    journey_id: str = Field(default="", max_length=80)
    message: str = Field(default="", max_length=2000)
    recipe_id: str = Field(default="shakshuka", max_length=80)
    expected_revision: int = Field(default=0, ge=0)
    answer: str = Field(default="", max_length=120)
    question_id: str = Field(default="", max_length=80)
    problem_id: str = Field(default="", max_length=80)
    chefPersonality: str = Field(default="professional", pattern="^(supportive|professional|tough)$")
    temperature: float | None = Field(default=None, ge=-50, le=300, allow_inf_nan=False)
    hazard_resolved: bool = False
    allergies: list[str] = Field(default_factory=list, max_length=30)
    seconds: int = Field(default=180, ge=1, le=14400)
    dish_title: str = Field(default="", max_length=200)
    method: str = Field(default="", max_length=160)
    ingredients: list[str] = Field(default_factory=list, max_length=100)
    step_title: str = Field(default="", max_length=160)
    step_instruction: str = Field(default="", max_length=1000)
    step_id: str = Field(default="", max_length=80)
    target_index: int = Field(default=0, ge=0, le=29)
    mode: str = Field(default="mentor", pattern="^(mentor|consultant)$")
    observation: str = Field(default="", max_length=80)
    graph_path_id: str = Field(default="", max_length=80)
    forbid_meat_dairy: bool = True
    rest_seconds: int | None = Field(default=None, ge=0, le=3600)


class JourneyState(StrictModel):
    id: str = Field(max_length=80)
    recipe_id: str = Field(max_length=80)
    revision: int = Field(ge=1)
    current_step: int = Field(ge=0, le=30)
    stage_valid: bool = False
    safety_hold: bool = False
    status: str = Field(pattern="^(active|paused|completed)$")
    chefPersonality: str = Field(pattern="^(supportive|professional|tough)$")
    step_started_at: float
    last_user_at: float
    timer_deadline: float | None = None
    paused_remaining: float | None = None
    check_due_at: float | None = None
    asked: list[str] = Field(default_factory=list, max_length=10)
    messages: list[CoachMessage] = Field(default_factory=list, max_length=60)
    workflow: str = Field(default="guided", pattern="^(guided|user)$")
    mode: str = Field(default="mentor", pattern="^(mentor|consultant)$")
    checkin_seconds: int = Field(default=180, ge=60, le=3600)
    dish_title: str = Field(default="", max_length=200)
    original_dish_title: str = Field(default="", max_length=200)
    allergies: list[str] = Field(default_factory=list, max_length=30)
    method: str = Field(default="", max_length=160)
    ingredients: list[str] = Field(default_factory=list, max_length=100)
    custom_steps: list[SmartStep] = Field(default_factory=list, max_length=30)
    completed_step_ids: list[str] = Field(default_factory=list, max_length=30)
    context: DishContext | None = None
    learning_focus: ContextTip | None = None
    issues: list[str] = Field(default_factory=list, max_length=20)
    report_count: int = Field(default=0, ge=0)
    measured_temperature: float | None = Field(default=None, allow_inf_nan=False, ge=-50, le=300)
    completion_summary: list[str] = Field(default_factory=list, max_length=10)
    forbid_meat_dairy: bool = True
    measured_rest_seconds: int | None = Field(default=None, ge=0, le=3600)
    applied_graph_rules: list[str] = Field(default_factory=list, max_length=100)
    decision_answers: dict[str, str] = Field(default_factory=dict, max_length=20)
    decision_questions: list[DecisionQuestion] = Field(default_factory=list, max_length=8)
    problem_options: list[dict] = Field(default_factory=list, max_length=20)
    problem_rule_status: str = ""
    problem_questions: list[DecisionQuestion] = Field(default_factory=list, max_length=4)
    pending_problem: dict = Field(default_factory=dict)
    problem_rule_match: dict = Field(default_factory=dict)
    missing_problem_rules: list[dict] = Field(default_factory=list, max_length=30)
    method_recommendations: dict = Field(default_factory=dict)
    method_warning: str = Field(default="", max_length=1000)


class PreviewRequest(StrictModel):
    state: JourneyState | None = None
    command: CoachCommand


def say(state, text, kind="chef"):
    prefix = {"supportive": "אני איתך. ", "professional": "", "tough": "שים לב. "}[state["chefPersonality"]]
    state["messages"] = (
        state["messages"] + [{"role": kind, "text": prefix + text if kind == "chef" else text}]
    )[-60:]


def apply_command(previous, command, now=None, problem_rules=None, method_policy=None):
    now = datetime.now(UTC).timestamp() if now is None else now
    if command.action == "start_custom":
        from app.consultant import start_user_work

        return start_user_work(command, now, problem_rules, method_policy)
    if command.action == "start":
        if command.recipe_id not in RECIPES:
            raise DomainError("NOT_FOUND", "Recipe not found", 404)
        aliases = {"eggs": {"eggs", "egg", "ביצה", "ביצים"}, "wheat": {"wheat", "gluten", "חיטה", "גלוטן"}}
        avoided = {value.strip().lower() for value in command.allergies}
        if any(
            avoided & aliases.get(allergen, {allergen})
            for allergen in RECIPES[command.recipe_id]["allergens"]
        ):
            raise DomainError(
                "ALLERGEN_CONFLICT", "The selected dish contains an allergen in your avoidance profile", 422
            )
        state = JourneyState(
            id="coach_" + uuid4().hex,
            recipe_id=command.recipe_id,
            revision=1,
            current_step=0,
            status="active",
            chefPersonality=command.chefPersonality,
            step_started_at=now,
            last_user_at=now,
        ).model_dump()
        say(state, "נתחיל בהכנה. " + RECIPES[state["recipe_id"]]["steps"][0]["chefQuestions"][0])
        return state
    if previous is None or (previous.get("workflow") != "user" and previous["recipe_id"] not in RECIPES):
        raise DomainError("NOT_FOUND", "Journey not found", 404)
    state = deepcopy(previous)
    if command.expected_revision != state["revision"]:
        raise DomainError("STATE_CONFLICT", "Reload current cooking state", 409)
    if state.get("workflow") == "user":
        from app.consultant import apply_user_command

        return apply_user_command(state, command, now, problem_rules, method_policy)
    steps = RECIPES[state["recipe_id"]]["steps"]
    if state["current_step"] >= len(steps):
        raise DomainError("INVALID_REQUEST", "Invalid current step", 422)
    current = steps[state["current_step"]]
    if command.action == "personality":
        state["chefPersonality"] = command.chefPersonality
    elif state["status"] == "completed":
        raise DomainError("JOURNEY_COMPLETED", "Start a new journey to continue", 409)
    elif command.action == "pause":
        if state["status"] == "active":
            state["paused_remaining"] = (
                max(0, state["timer_deadline"] - now) if state["timer_deadline"] else None
            )
            state["timer_deadline"] = None
            state["status"] = "paused"
            say(state, "הליווי מושהה. ההשהיה באפליקציה אינה מכבה את הכיריים או התנור.")
    elif command.action == "resume":
        if state["status"] == "paused":
            if state["safety_hold"] and not command.hazard_resolved:
                raise DomainError("SAFETY_HOLD", "Confirm the hazard was resolved before resuming", 409)
            state["safety_hold"] = False
            state["status"] = "active"
            remaining = state["paused_remaining"]
            state["timer_deadline"] = now + remaining if remaining is not None else None
            state["check_due_at"] = state["timer_deadline"]
            state["last_user_at"] = now
            say(state, "חזרנו. " + current["chefQuestions"][0])
    elif state["status"] != "active":
        raise DomainError("JOURNEY_PAUSED", "Resume before updating the step", 409)
    elif command.action == "check_in":
        if (
            state["check_due_at"] is not None
            and now >= state["check_due_at"]
            and "time" not in state["asked"]
        ):
            say(state, "הגיע זמן לבדיקה, לא לסיום אוטומטי. " + current["chefQuestions"][0])
            state["asked"].append("time")
        elif now - state["last_user_at"] >= 180 and "idle" not in state["asked"]:
            say(state, "האם אתה עדיין בשלב הזה? צריך עזרה?")
            state["asked"].append("idle")
        else:
            return state
    elif command.action == "timer_cancel":
        state["timer_deadline"] = state["check_due_at"] = state["paused_remaining"] = None
        state["asked"] = [key for key in state["asked"] if key != "time"]
        say(state, "התזכורת בוטלה.")
    elif command.action == "timer":
        state["timer_deadline"] = now + command.seconds
        state["check_due_at"] = state["timer_deadline"]
        state["asked"] = [key for key in state["asked"] if key != "time"]
        say(state, "הופעלה תזכורת לבדיקה. היא אינה קובעת שהמזון מוכן.")
    elif command.action == "problem":
        state["stage_valid"] = False
        say(state, current["recoveryInstructions"][0] + " " + current["chefQuestions"][0])
    elif command.action == "ask":
        if not command.message.strip():
            raise DomainError("INVALID_REQUEST", "A question is required", 422)
        say(state, command.message, "user")
        if any(term in command.message.lower() for term in ("עולה באש", "בוער", "oil fire", "pan on fire")):
            state["stage_valid"] = False
            state["status"] = "paused"
            state["safety_hold"] = True
            state["paused_remaining"] = None
            state["timer_deadline"] = None
            say(state, "עצור את הבישול וטפל בסיכון לפני כל המשך. המערכת אינה יכולה לאשר שהמצב בטוח.")
        elif any(term in command.message.lower() for term in ("למה", "why", "הסבר")):
            say(state, current["why"])
        elif any(
            term in command.message.lower() for term in ("נשרף", "שרוף", "בעיה", "נדבק", "burn", "problem")
        ):
            state["stage_valid"] = False
            say(state, current["recoveryInstructions"][0])
        else:
            say(
                state,
                "בהקשר לשלב הנוכחי: "
                + current["instruction"]
                + " לבדיקה: "
                + current["successCriteria"][0]
                + ". "
                + current["chefQuestions"][0],
            )
    elif command.action == "answer":
        if current["minimum_temperature"] is not None:
            if command.temperature is None:
                raise DomainError("INVALID_REQUEST", "A measured temperature is required", 422)
            state["stage_valid"] = command.temperature >= current["minimum_temperature"]
            say(state, f"דיווחת על {command.temperature:g}°C.", "user")
            say(
                state,
                "המדידה שדיווחת עומדת בסף. אפשר לסיים את השלב."
                if state["stage_valid"]
                else current["recoveryInstructions"][0],
            )
        else:
            option = next((option for option in current["options"] if option["id"] == command.answer), None)
            if option is None:
                raise DomainError("INVALID_REQUEST", "Choose an available answer", 422)
            say(state, option["label"], "user")
            state["stage_valid"] = option["result"] == "pass"
            say(state, option["response"])
    elif command.action == "complete":
        if not state["stage_valid"]:
            say(state, "לפני שמתקדמים: " + current["chefQuestions"][0])
        elif state["current_step"] + 1 == len(steps):
            state["status"] = "completed"
            state["timer_deadline"] = None
            say(state, "סיימת את המסלול לפי הבדיקות שדיווחת. בתיאבון!")
        else:
            state["current_step"] += 1
            state["stage_valid"] = False
            state["step_started_at"] = now
            state["asked"] = []
            next_step = steps[state["current_step"]]
            duration = next_step["check_after_seconds"]
            state["timer_deadline"] = now + duration if duration else None
            state["check_due_at"] = state["timer_deadline"]
            say(state, next_step["instruction"] + " " + next_step["chefQuestions"][0])
    if command.action != "check_in":
        state["last_user_at"] = now
        state["asked"] = [key for key in state["asked"] if key != "idle"]
    state["revision"] += 1
    return state


def install_coach_routes(app, principal, db):
    @app.get("/v1/coach/graph/catalog")
    def graph_catalog():
        data = graph()
        return {
            "ingredients": list(data["ingredients"].values()),
            "methods": list(data["methods"].values()),
            "paths": data["paths"],
            "source_sha256": data["sha256"],
            "domain_source_sha256": data["domain_sha256"],
            "review_status": "ADAPTED_NOT_PROFESSIONALLY_VALIDATED",
        }

    @app.get("/v1/coach/graph/audit")
    def graph_audit(owner=Depends(principal)):
        return audit_graph()

    @app.get("/v1/coach/recipes")
    def recipes():
        return {
            "items": list(RECIPES.values()),
            "notice": "מסלולי פתיחה שנכתבו למערכת; לא נבדקו מקצועית במטבח. זמני התזכורות משוערים.",
        }

    @app.post("/v1/coach/preview")
    def preview(body: PreviewRequest):
        return apply_command(body.state.model_dump() if body.state else None, body.command)

    @app.get("/v1/coach/current")
    def current(owner=Depends(principal), session=Depends(db)):
        record = session.scalar(
            select(CookingRecord)
            .where(
                CookingRecord.owner_id == owner.user_id, CookingRecord.state["kind"].as_string() == "coach"
            )
            .order_by(CookingRecord.state["updated_at"].as_string().desc())
            .limit(1)
        )
        journey = deepcopy(record.state["journey"]) if record else None
        if journey and journey.get("workflow") == "user":
            from app.decision_table import refresh_decisions
            from app.method_policy import attach_recommendations, effective_policy
            from app.problem_rules import effective_rules, options

            attach_recommendations(journey, effective_policy(session, owner.user_id)["policy"])
            refresh_decisions(journey)
            journey["problem_options"] = options(journey, effective_rules(session, owner.user_id)["rules"])
        return {"journey": journey}

    @app.post("/v1/coach/events")
    def event(body: CoachCommand, owner=Depends(principal), session=Depends(db)):
        record = session.scalar(
            select(CookingRecord)
            .where(
                CookingRecord.owner_id == owner.user_id, CookingRecord.state["kind"].as_string() == "coach"
            )
            .order_by(CookingRecord.state["updated_at"].as_string().desc())
            .limit(1)
            .with_for_update()
        )
        previous = record.state["journey"] if record else None
        if body.action not in ("start", "start_custom") and (
            previous is None or body.journey_id != previous["id"]
        ):
            raise DomainError("STATE_CONFLICT", "The active journey changed; reload it", 409)
        from app.method_policy import effective_policy
        from app.problem_rules import effective_rules

        state = apply_command(
            previous,
            body,
            problem_rules=effective_rules(session, owner.user_id)["rules"],
            method_policy=effective_policy(session, owner.user_id)["policy"],
        )
        if body.action in ("start", "start_custom"):
            record = CookingRecord(owner_id=owner.user_id, cooking_id=state["id"])
            session.add(record)
        elif state["revision"] == previous["revision"]:
            return state
        record.revision = state["revision"]
        record.state = {"kind": "coach", "journey": state, "updated_at": datetime.now(UTC).isoformat()}
        record.decision = {"instruction": state["messages"][-1]["text"]}
        audit(
            session,
            owner.user_id,
            "COACH_EVENT",
            cooking_id=state["id"],
            action_type=body.action,
            revision=state["revision"],
        )
        session.commit()
        return state
