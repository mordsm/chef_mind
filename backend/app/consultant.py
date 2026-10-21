"""User-directed workbench: the cook owns the plan; advice never silently changes it."""

from copy import deepcopy
from uuid import uuid4

from app.culinary_context import contextual_reply, dish_context
from app.decision_table import accept_decision, refresh_decisions
from app.knowledge import DomainError
from app.knowledge_graph import dietary_paths, observation_reply
from app.method_policy import attach_recommendations, effective_policy, enforce_method
from app.problem_rules import accept_problem_choice, effective_rules, identify_problem, options, problem_reply


def check_ingredient_avoidance(ingredients, avoided):
    groups = [
        {"milk", "חלב", "cheese", "גבינה", "butter", "חמאה", "cream", "שמנת"},
        {"egg", "eggs", "ביצה", "ביצים"},
        {"wheat", "חיטה", "קמח חיטה", "gluten", "גלוטן"},
        {"fish", "דג", "דגים"},
        {"peanuts", "בוטנים"},
        {"sesame", "שומשום", "טחינה"},
        {"soy", "סויה", "טופו"},
    ]
    names = {item.strip().lower() for item in ingredients}
    avoidance = {item.strip().lower() for item in avoided}
    if any(names & group and avoidance & group for group in groups):
        raise DomainError(
            "ALLERGEN_CONFLICT", "A reported ingredient conflicts with the avoidance profile", 422
        )


def start_user_work(command, now, problem_rules=None, method_policy=None):
    from app.coach import JourneyState, say

    if not command.dish_title.strip():
        raise DomainError("INVALID_REQUEST", "A dish name is required", 422)
    if any(not item.strip() or len(item) > 160 for item in command.ingredients):
        raise DomainError("INVALID_REQUEST", "Ingredient names must be bounded and nonempty", 422)
    policy = method_policy if method_policy is not None else effective_policy()["policy"]
    selected_method = enforce_method(command.dish_title, command.method, command.ingredients, policy)
    context = dish_context(command.dish_title, selected_method, command.ingredients)
    context["graph"] = dietary_paths(context["graph"], command.allergies, command.forbid_meat_dairy)
    check_ingredient_avoidance(command.ingredients, command.allergies)
    state = JourneyState(
        id="coach_" + uuid4().hex,
        recipe_id="custom",
        revision=1,
        current_step=0,
        status="active",
        chefPersonality=command.chefPersonality,
        step_started_at=now,
        last_user_at=now,
        workflow="user",
        mode=command.mode,
        checkin_seconds=300 if command.mode == "mentor" else 600,
        dish_title=command.dish_title,
        original_dish_title=command.dish_title,
        allergies=command.allergies,
        forbid_meat_dairy=command.forbid_meat_dairy,
        method=selected_method,
        ingredients=command.ingredients,
        context=context,
    ).model_dump()
    say(state, f"אתה מכין {command.dish_title}. השלבים וההחלטות שלך; אפשר להוסיף פעולה או לדווח מה כבר עשית.")
    opening = [context["tips"][0]["text"]]
    opening.extend(tip["text"] for tip in context["tips"] if tip["origin"] == "SAFETY_POLICY")
    say(state, "\n\n".join(dict.fromkeys(opening)))
    attach_recommendations(state, policy)
    refresh_decisions(state)
    state["problem_options"] = options(
        state, problem_rules if problem_rules is not None else effective_rules()["rules"]
    )
    return state


def user_step(title, instruction, context, step_id=None):
    from app.coach import step

    result = step(
        title,
        instruction or title,
        context["tips"][0]["text"],
        "סיום הפעולה לפי דיווח המשתמש",
        "מה המצב כעת ומה תרצה לעשות בהמשך?",
        failure="פער בין התוצאה שציפית לה לבין המצב בפועל",
        recovery="תאר מה השתנה ובקש עזרה לפני בחירת תיקון.",
    )
    result["id"] = step_id or uuid4().hex
    result["source"] = "USER_PROVIDED"
    return result


def apply_user_command(state, command, now, problem_rules=None, method_policy=None):
    from app.coach import say

    state = deepcopy(state)
    previous_method_value = state["method"]
    # Re-derive safety/context from reported ingredients, not client-provided advice fields.
    context = dish_context(state["dish_title"], state["method"], state["ingredients"])
    context["graph"] = dietary_paths(
        context["graph"], state["allergies"], state.get("forbid_meat_dairy", True)
    )
    state["context"] = context
    policy = method_policy if method_policy is not None else effective_policy()["policy"]
    attach_recommendations(state, policy)
    state.setdefault("decision_answers", {})
    refresh_decisions(state)
    rules = problem_rules if problem_rules is not None else effective_rules()["rules"]
    state["problem_options"] = options(state, rules)
    steps = state["custom_steps"]
    current = steps[state["current_step"]] if steps and state["current_step"] < len(steps) else None
    if command.action == "personality":
        state["chefPersonality"] = command.chefPersonality
    elif command.action == "mode":
        state["mode"] = command.mode
        state["checkin_seconds"] = 300 if command.mode == "mentor" else 600
        say(state, "הליווי יעודכן לפי המצב שבחרת. בדיקות בטיחות נשארות בתוקף.")
    elif state["status"] == "completed":
        raise DomainError("JOURNEY_COMPLETED", "The user ended this cooking session", 409)
    elif command.action == "finish":
        state["status"] = "completed"
        state["timer_deadline"] = state["check_due_at"] = None
        summary = [
            f"סיימת את העבודה על {state['dish_title']} לפי החלטתך.",
            f"נרשמו {state['report_count']} דיווחים ו־{len(state['completed_step_ids'])} פעולות שסימנת כהושלמו.",
        ]
        if state["issues"]:
            summary.append("נושאים שעלו: " + ", ".join(state["issues"]) + ". לא דווח בהכרח שטופלו.")
            summary.append(
                "לפעם הבאה: בדוק את מצב המנה לפני שינוי חום, נוזלים או תיבול; בצע שינוי אחד בכל פעם."
            )
        minimum = context["minimum_temperature"]
        if minimum is not None:
            measured = state["measured_temperature"]
            summary.append(
                f"דיווחת על מדידה של {measured:g}°C מול סף {minimum:g}°C; אין בכך אימות עצמאי של המנה."
                if measured is not None and measured >= minimum
                else "לא דווחה מדידה שעומדת בסף; סיום העבודה אינו אישור שהמזון מוכן או בטוח."
            )
        if context.get("minimum_rest_seconds", 0) > (state.get("measured_rest_seconds") or 0):
            summary.append("לא דווח זמן מנוחה שעומד בדרישה לחומר הגלם.")
        if context["graph"]["method"] and context["graph"]["method"]["requires_validated_process"]:
            summary.append("תהליך ההכנה בשיטה שנבחרה לא אומת במערכת.")
        if state["safety_hold"]:
            summary.append("נרשם סיכון שטרם אושר שטופל.")
        state["completion_summary"] = summary
        say(state, " ".join(summary))
    elif command.action == "pause":
        if state["status"] == "active":
            state["paused_remaining"] = (
                max(0, state["timer_deadline"] - now) if state["timer_deadline"] else None
            )
            state["timer_deadline"] = None
            state["status"] = "paused"
            say(state, "הליווי מושהה. זו אינה פעולה שמכבה את מקור החום.")
    elif command.action == "resume":
        if state["safety_hold"] and not command.hazard_resolved:
            raise DomainError("SAFETY_HOLD", "Confirm the hazard was resolved", 409)
        state["safety_hold"] = False
        if state["status"] == "paused":
            state["status"] = "active"
            state["timer_deadline"] = (
                now + state["paused_remaining"] if state["paused_remaining"] is not None else None
            )
            state["check_due_at"] = state["timer_deadline"]
            say(state, "חזרנו. מה השתנה מאז הדיווח האחרון?")
    elif command.action == "timer_cancel":
        state["timer_deadline"] = state["check_due_at"] = state["paused_remaining"] = None
        state["asked"] = [key for key in state["asked"] if key != "time"]
        say(state, "התזכורת בוטלה.")
    elif state["status"] != "active":
        raise DomainError("JOURNEY_PAUSED", "Resume before updating", 409)
    elif command.action == "check_in":
        if (
            state["check_due_at"] is not None
            and now >= state["check_due_at"]
            and "time" not in state["asked"]
        ):
            state["asked"].append("time")
            say(state, "הגיע זמן התזכורת שבחרת. מה מצב המנה כעת?")
        elif now - state["last_user_at"] >= state["checkin_seconds"] and "idle" not in state["asked"]:
            state["asked"].append("idle")
            say(state, "עבר זמן מאז הדיווח האחרון. האם אתה עדיין בפעולה הזו, ומה מצב המנה? צריך עזרה?")
        else:
            return state
    elif command.action == "timer":
        state["timer_deadline"] = state["check_due_at"] = now + command.seconds
        state["asked"] = [item for item in state["asked"] if item != "time"]
        say(state, "נרשמה תזכורת לבדיקה בזמן שבחרת. אין מעבר אוטומטי בין פעולות.")
    elif command.action == "update_plan":
        if not command.dish_title.strip() or any(
            not item.strip() or len(item) > 160 for item in command.ingredients
        ):
            raise DomainError("INVALID_REQUEST", "Valid dish and ingredient names are required", 422)
        check_ingredient_avoidance(command.ingredients, state["allergies"])
        selected_method = enforce_method(command.dish_title, command.method, command.ingredients, policy)
        state["dish_title"], state["method"], state["ingredients"] = (
            command.dish_title,
            selected_method,
            command.ingredients,
        )
        state["context"] = dish_context(command.dish_title, selected_method, command.ingredients)
        state["forbid_meat_dairy"] = command.forbid_meat_dairy
        state["context"]["graph"] = dietary_paths(
            state["context"]["graph"], state["allergies"], command.forbid_meat_dairy
        )
        state["measured_rest_seconds"] = None
        state["measured_temperature"] = None
        state["learning_focus"] = None
        state["decision_answers"] = {}
        state["pending_problem"] = {}
        state["problem_questions"] = []
        state["problem_rule_match"] = {}
        state["problem_rule_status"] = ""
        say(
            state,
            "פרטי המנה עודכנו לפי בחירתך. הפעולות שלך נשמרו; המדידה הקודמת אינה משמשת לאישור ההרכב המעודכן.",
        )
    elif command.action == "adopt_path":
        path = next((item for item in context["graph"]["paths"] if item["id"] == command.graph_path_id), None)
        if not path or not path["selectable"]:
            raise DomainError("INVALID_REQUEST", "Choose an available relevant path", 422)
        enforce_method(state["dish_title"], path["method_ref"], state["ingredients"], policy)
        additions = path["detailed_steps"] or [
            {"title": title, "instruction": title} for title in path["suggestions"]
        ]
        if len(steps) + len(additions) > 30:
            raise DomainError("INVALID_REQUEST", "At most 30 steps", 422)
        for detail in additions:
            item = user_step(detail["title"], detail["instruction"], context)
            for field in (
                "why",
                "commonMistakes",
                "successCriteria",
                "recoveryActions",
                "chefQuestions",
                "next_step_prep",
            ):
                if field in detail:
                    item[field] = detail[field]
            item["source"] = "USER_GRAPH_ADAPTED:" + detail.get("source_id", path["source_id"])
            steps.append(item)
        state["applied_graph_rules"] = list(
            dict.fromkeys(
                state.get("applied_graph_rules", []) + [path["source_id"], path["domain_source_id"]]
            )
        )[-100:]
        say(state, "המתווה נוסף לפי בחירתך. אפשר לערוך את הפעולות; זמני המקור אינם מופעלים אוטומטית.")
    elif command.action == "add_step":
        if len(steps) >= 30 or not command.step_title.strip():
            raise DomainError("INVALID_REQUEST", "Choose a nonempty title; at most 30 steps", 422)
        steps.append(user_step(command.step_title, command.step_instruction, context))
        if len(steps) == 1:
            state["current_step"] = 0
        say(state, f"הפעולה שהוספת נרשמה: {command.step_title}. אפשר לערוך או לבחור פעולה אחרת.")
    elif command.action in ("edit_step", "remove_step", "select_step", "move_step"):
        index = next((i for i, item in enumerate(steps) if item["id"] == command.step_id), None)
        if index is None:
            raise DomainError("NOT_FOUND", "Step not found", 404)
        current_id = current["id"] if current else None
        if command.action == "edit_step":
            if not command.step_title.strip():
                raise DomainError("INVALID_REQUEST", "A step title is required", 422)
            steps[index] = user_step(command.step_title, command.step_instruction, context, command.step_id)
        elif command.action == "remove_step":
            steps.pop(index)
            state["completed_step_ids"] = [
                value for value in state["completed_step_ids"] if value != command.step_id
            ]
        elif command.action == "move_step":
            item = steps.pop(index)
            steps.insert(min(command.target_index, len(steps)), item)
        if command.action == "select_step":
            state["current_step"] = index
        else:
            state["current_step"] = next(
                (i for i, item in enumerate(steps) if item["id"] == current_id),
                min(state["current_step"], max(0, len(steps) - 1)),
            )
    elif command.action == "complete":
        if not current:
            say(state, "אפשר להוסיף פעולה משלך, או פשוט לדווח מה עשית. אין צורך להשלים תסריט של המערכת.")
        else:
            if current["id"] not in state["completed_step_ids"]:
                state["completed_step_ids"].append(current["id"])
            next_index = next(
                (i for i, item in enumerate(steps) if item["id"] not in state["completed_step_ids"]), None
            )
            if next_index is not None:
                state["current_step"] = next_index
            say(
                state,
                "רשמתי שסיימת את הפעולה לפי הדיווח שלך. אתה בוחר אם להמשיך לפעולה אחרת או לסיים את העבודה.",
            )
    elif command.action in ("report", "ask", "answer", "problem"):
        problem = identify_problem(command)
        decision = None
        if (
            not problem
            and command.action != "problem"
            and (
                command.question_id
                or command.answer
                or (
                    command.message
                    and command.temperature is None
                    and command.rest_seconds is None
                    and not command.observation
                )
            )
        ):
            decision = (
                accept_problem_choice(state, command, rules)
                if command.question_id.startswith("problem_")
                else accept_decision(state, command)
            )
        rule = observation_reply(context["graph"], command.observation) if command.observation else None
        if command.observation and not rule:
            raise DomainError("INVALID_REQUEST", "Observation does not belong to this method", 422)
        if rule:
            text = rule["label"]
        elif command.rest_seconds is not None:
            state["measured_rest_seconds"] = command.rest_seconds
            text = f"דיווח מנוחה לאחר הבישול: {command.rest_seconds} שניות"
        elif command.temperature is not None:
            state["measured_temperature"] = command.temperature
            text = f"דיווח מדידה בחלקים העבים: {command.temperature:g}°C"
        else:
            text = (
                command.message.strip()
                or (
                    next(
                        (option["label"] for option in state["problem_options"] if option["id"] == problem),
                        "",
                    )
                    if problem
                    else ""
                )
                or (decision[1] if decision else "")
                or ("יש בעיה" if command.action == "problem" else "")
            )
            if decision and not text:
                text = "בחירה לא מזוהה"
        if not text:
            raise DomainError("INVALID_REQUEST", "A report or question is required", 422)
        say(state, text, "user")
        state["report_count"] += 1
        if problem == "fire" or any(
            term in text.lower() for term in ("עולה באש", "בוער", "oil fire", "pan on fire")
        ):
            state["problem_rule_status"] = "safety"
            state["pending_problem"] = {}
            state["problem_questions"] = []
            state["problem_rule_match"] = {}
            state["safety_hold"] = True
            state["status"] = "paused"
            state["timer_deadline"] = state["check_due_at"] = state["paused_remaining"] = None
            if "סיכון אש" not in state["issues"]:
                state["issues"] = (state["issues"] + ["סיכון אש"])[-20:]
            say(state, "עצור את הבישול וטפל בסיכון לפני המשך. המערכת אינה יכולה לאשר שהמצב בטוח.")
        elif problem or command.action == "problem" or "יש בעיה" in text:
            if problem:
                reply = problem_reply(state, problem, text, rules)
            else:
                state["problem_rule_status"] = "choose"
                reply = "מה הבעיה? בחר מהאפשרויות המוצגות כדי לקבל תשובה לפי חוק. אם הבעיה אינה ברשימה, בחר ״בעיה אחרת״ ותאר אותה."
            state["learning_focus"] = {"title": "טיפול בבעיה", "text": reply, "source": ""}
            say(state, reply)
        elif decision:
            if state["method"] != previous_method_value:
                enforce_method(state["dish_title"], state["method"], state["ingredients"], policy)
            reply, label = decision
            state["learning_focus"] = {"title": label or "בחירת אפשרות", "text": reply, "source": ""}
            say(state, reply)
            state["context"] = dish_context(state["dish_title"], state["method"], state["ingredients"])
            state["context"]["graph"] = dietary_paths(
                state["context"]["graph"], state["allergies"], state["forbid_meat_dairy"]
            )
        elif rule:
            state["learning_focus"] = {
                "title": rule["label"],
                "text": rule["message"],
                "source": "",
                "origin": "USER_GRAPH_ADAPTED",
                "source_ids": [rule["source_id"]],
            }
            state["applied_graph_rules"] = list(
                dict.fromkeys(state.get("applied_graph_rules", []) + [rule["source_id"]])
            )[-100:]
            if rule["severity"] == "safety":
                state["safety_hold"] = True
                state["status"] = "paused"
                state["timer_deadline"] = state["check_due_at"] = state["paused_remaining"] = None
                state["issues"] = list(dict.fromkeys(state["issues"] + [rule["label"]]))[-20:]
            say(state, rule["message"])
        elif command.rest_seconds is not None:
            say(state, "זמן המנוחה נרשם לפי דיווחך; הוא אינו מחליף מדידת ליבה או אימות תהליך.")
        elif (
            context["graph"]["method"]
            and context["graph"]["method"]["requires_validated_process"]
            and command.temperature is not None
        ):
            say(state, "המדידה נרשמה. בשיטה זו טמפרטורה בודדת אינה מאמתת תהליך או מוכנות להגשה.")
        elif command.temperature is not None and context["minimum_temperature"] is not None:
            minimum = context["minimum_temperature"]
            say(
                state,
                f"המדידה שדיווחת עומדת בסף של {minimum:g}°C; אין בכך אימות עצמאי."
                if command.temperature >= minimum
                else f"המדידה נמוכה מסף {minimum:g}°C. אין אישור מוכנות; המשך לפי שיטת ההכנה ובדוק שוב.",
            )
        else:
            reply, issue = contextual_reply(
                context, text, current["title"] if current else "", state["mode"] == "consultant"
            )
            if not issue and current and current["source"].startswith("USER_GRAPH_ADAPTED:"):
                reply = current["instruction"] + " " + current["chefQuestions"][0]
            if command.action == "report":
                reply = "הדיווח התקבל: " + text[:240] + "\n\n" + reply
            state["learning_focus"] = {"title": issue or "בהקשר לדיווח האחרון", "text": reply, "source": ""}
            if current and current["source"].startswith("USER_GRAPH_ADAPTED:") and not issue:
                state["learning_focus"].update(
                    origin="USER_GRAPH_ADAPTED", source_ids=[current["source"].split(":", 1)[1]]
                )
            if issue and issue not in state["issues"]:
                state["issues"] = (state["issues"] + [issue])[-20:]
            say(state, reply)
    else:
        raise DomainError("INVALID_REQUEST", "This action is not supported in user-directed work", 422)
    if command.action != "check_in":
        state["last_user_at"] = now
        state["asked"] = [item for item in state["asked"] if item != "idle"]
    attach_recommendations(state, policy)
    refresh_decisions(state)
    state["revision"] += 1
    return state
