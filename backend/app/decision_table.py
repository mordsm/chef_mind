"""Explicit local choices, numeric answers and exact aliases; no model interpretation."""

import re

from pydantic import Field

from app.knowledge import DomainError
from app.schemas import StrictModel


class DecisionOption(StrictModel):
    id: str
    label: str
    number: int


class DecisionQuestion(StrictModel):
    id: str
    text: str
    options: list[DecisionOption] = Field(max_length=8)


# id, label, exact text aliases, response, optional method selected by the cook.
METHODS = [
    (
        "simmer",
        "בישול בנוזל בסיר",
        ["סיר", "בישול בנוזל"],
        "נבחר בישול בנוזל. בדוק שיש נוזל ושאפשר לשלוט בבעבוע; הרכות נבדקת במהלך העבודה בנפרד מבטיחות.",
        "בישול בנוזל",
    ),
    (
        "pressure",
        "סיר לחץ",
        [],
        "נבחר סיר לחץ. השתמש בהוראות היצרן לדגם, לכמות ולשחרור לחץ; אין במערכת תוכנית לחץ מאומתת או זמן אחיד.",
        "סיר לחץ",
    ),
    (
        "pan",
        "מחבת",
        [],
        "נבחרה מחבת. אם המטרה קורקבנים רכים, ספר אם כבר בושלו לפני ההשחמה; השחמה לבדה אינה מעידה על רכות או בטיחות.",
        "מחבת",
    ),
    (
        "undecided",
        "עדיין לא בחרתי שיטה",
        ["לא בחרתי"],
        "השיטה נשארת פתוחה. אפשר להתחיל בבירור מצב חומרי הגלם והתוצאה הרצויה לפני הפעלת חום.",
        "",
    ),
]
CONDITION = [
    (
        "fresh_clean",
        "טריים ומנוקים",
        ["טריים"],
        "נרשם: קורקבנים טריים ומנוקים לפי דיווחך. שמור בקירור עד ההכנה.",
        "",
    ),
    (
        "thawed_clean",
        "מופשרים ומנוקים",
        ["מופשרים"],
        "נרשם: מופשרים ומנוקים לפי דיווחך. שמור בקירור והפרד כלים שנגעו בעוף נא.",
        "",
    ),
    (
        "frozen",
        "עדיין קפואים",
        ["קפואים"],
        "נרשם שהם עדיין קפואים. קודם יש לברר הפשרה ושיטת הכנה מתאימות; אין להסיק מהזמן או מהצבע שהם מוכנים.",
        "",
    ),
    (
        "unknown",
        "לא בטוח אם מופשרים או מנוקים",
        ["לא בטוח"],
        "מצב חומרי הגלם אינו ברור. בדוק את האריזה והמצב בפועל לפני תחילת ההכנה.",
        "",
    ),
]
GOAL = [
    (
        "sauce",
        "תבשיל רך ברוטב",
        ["רך ברוטב", "ברוטב", "רוצה תבשיל רך ברוטב"],
        "בחרת תבשיל רך ברוטב. הכיוון הוא בישול בנוזל ובדיקת רכות במהלך העבודה; השחמה אינה שלב חובה. הבחירה נשמרה בלי לשנות את הפעולות בתוכנית שלך.",
        "",
    ),
    (
        "brown",
        "השחמה בסיום",
        ["השחמה", "רוצה השחמה בסיום"],
        "בחרת השחמה בסיום. נברר קודם אם הקורקבנים כבר בושלו ורוככו; צבע ההשחמה אינו בדיקת בטיחות.",
        "",
    ),
    (
        "undecided",
        "עדיין לא החלטתי על התוצאה",
        [],
        "התוצאה עדיין פתוחה. אפשר לבחור בה לאחר בירור מצב חומרי הגלם ושיטת ההכנה.",
        "",
    ),
]
PROGRESS = [
    (
        "not_started",
        "עדיין לא התחלתי",
        ["טרם התחלתי"],
        "מתחילים מהכנות: בדוק חומרי גלם, כלים ושיטת הכנה לפני הפעלת חום. מה תרצה להכין קודם?",
        "",
    ),
    (
        "cooking",
        "כבר התחלתי לבשל",
        ["כבר מבשל"],
        "נרשם שכבר התחלת. דווח מה עשית ומה המצב בפועל כדי שאציע בדיקה מתאימה; אין התקדמות אוטומטית.",
        "",
    ),
    (
        "finishing",
        "לקראת סיום",
        [],
        "נרשם שאתה לקראת סיום. בדיקות מוכנות תלויות בחומרי הגלם ובשיטה; דווח מה מצב המנה ומה נמדד.",
        "",
    ),
]


def normalize(value):
    return re.sub(r"[\s.,!?؟]+", " ", value.casefold()).strip()


def definitions(state):
    text = " ".join([state["dish_title"], *state["ingredients"]]).casefold()
    nodes = state["context"]["graph"]["ingredients"]
    gizzards = any(node["id"] == "chicken_giblets" for node in nodes) and any(
        word in text for word in ("קורקבנ", "קורקבן", "קוקבנ", "קוקבן", "gizzard")
    )
    if not gizzards:
        return [("progress", "באיזה שלב אתה נמצא?", PROGRESS)]
    questions = [("condition", "מה מצב הקורקבנים?", CONDITION)]
    if not state["method"] or "method" in state.get("decision_answers", {}):
        questions.append(("method", "באיזו שיטה תרצה להכין?", METHODS))
    return [*questions, ("goal", "תבשיל רך ברוטב או השחמה בסיום?", GOAL)]


def refresh_decisions(state):
    answers = state.setdefault("decision_answers", {})
    questions = list(state.get("problem_questions", []))
    number = sum(len(q["options"]) for q in questions) + 1
    for key, text, options in definitions(state):
        if key == "method" and state.get("method_recommendations"):
            allowed = {item["id"] for item in state["method_recommendations"]["allowed"]}
            aliases = {"simmer": "boil_simmer", "pan": "pan_sear", "pressure": "pressure"}
            options = [
                option for option in options if option[0] == "undecided" or aliases.get(option[0]) in allowed
            ]
        if answers.get(key) in {option[0] for option in options}:
            continue
        choices = []
        for option in options:
            choices.append({"id": option[0], "label": option[1], "number": number})
            number += 1
        questions.append({"id": key, "text": text, "options": choices})
    state["decision_questions"] = questions


def accept_decision(state, command):
    """Return an explicit response or None for ordinary cooking dialogue."""
    refresh_decisions(state)
    question_id, choice_id = command.question_id, command.answer
    message = normalize(command.message)
    visible = [q for q in state["decision_questions"] if not q["id"].startswith("problem_")]
    if question_id or choice_id:
        question = next((q for q in visible if q["id"] == question_id), None)
        if not question or not any(option["id"] == choice_id for option in question["options"]):
            raise DomainError("INVALID_CHOICE", "Choose an option from a current question", 422)
    elif message.isdecimal():
        selected = [
            (q["id"], option["id"])
            for q in visible
            for option in q["options"]
            if str(option["number"]) == message
        ]
        if not selected:
            return "המספר אינו אחת האפשרויות המוצגות. בחר כפתור או הקלד את המספר שמופיע לידו.", ""
        question_id, choice_id = selected[0]
    elif message:
        matches = [
            (key, option[0])
            for key, _, options in definitions(state)
            for option in options
            if message in {normalize(value) for value in [option[1], *option[2]]}
        ]
        if len(matches) != 1:
            return None
        question_id, choice_id = matches[0]
    else:
        return None
    _, _, options = next(question for question in definitions(state) if question[0] == question_id)
    option = next(option for option in options if option[0] == choice_id)
    state["decision_answers"][question_id] = choice_id
    if question_id == "method" and option[4]:
        state["method"] = option[4]
    refresh_decisions(state)
    remaining = state["decision_questions"]
    reply = option[3]
    if remaining:
        reply += "\n\n" + remaining[0]["text"] + " בחר את האפשרות המתאימה בלחיצה."
    else:
        reply += "\n\nהבחירות נשמרו. כתוב מה כבר עשית ומה הכמות, או הוסף פעולה לתוכנית שלך."
    return reply, option[1]
