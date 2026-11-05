"""User-directed workbench: the cook owns the plan; advice never silently changes it."""

from copy import deepcopy
from uuid import uuid4

from app.book_knowledge import book_tips, enrich_context, practical_dish_tips
from app.cooking_intake import attach_intake, classification_ingredients, intake_reply
from app.cooking_operations import BY_ID, attach_operations, report_operation, select_operation
from app.culinary_context import contextual_reply, dish_context
from app.decision_table import accept_decision, refresh_decisions
from app.gizzard_guidance import preparation_guidance, report_guidance
from app.knowledge import DomainError
from app.knowledge_graph import dietary_paths, observation_reply
from app.method_policy import attach_recommendations, effective_policy, enforce_method
from app.problem_rules import accept_problem_choice, effective_rules, identify_problem, options, problem_reply
from app.salmon_guidance import PREP, add_salmon_paths, guide_oven_salmon, is_oven_salmon


def cooking_context(title, method="", ingredients=()):
    context = enrich_context(add_salmon_paths(dish_context(title, method, ingredients)), " ".join([title, method, *ingredients]))
    from app.culinary_context import strict_context
    return strict_context(context, title, ingredients)


def check_ingredient_avoidance(ingredients, avoided):
    from app.ingredient_safety import check_ingredients
    check_ingredients(ingredients, avoided)


def start_user_work(command, now, problem_rules=None, method_policy=None, recognition=None):
    from app.coach import JourneyState, say

    if not command.dish_title.strip():
        raise DomainError("INVALID_REQUEST", "A dish name is required", 422)
    if any(not item.strip() or len(item) > 160 for item in command.ingredients):
        raise DomainError("INVALID_REQUEST", "Ingredient names must be bounded and nonempty", 422)
    from app.ingredient_safety import check_ingredients
    check_ingredients(command.ingredients, command.allergies, command.forbid_meat_dairy)
    policy = method_policy if method_policy is not None else effective_policy()["policy"]
    identity = recognition or {'status':'rules_only'}
    facts = dict(identity.get('facts', {}))
    # Explicit user method or words in the title take precedence over model inference.
    from app.method_policy import canonical_method
    explicit_method = command.method or canonical_method(command.dish_title)
    requested_method = explicit_method or facts.get('method', '')
    try:
        selected_method = enforce_method(command.dish_title, requested_method, command.ingredients, policy)
    except DomainError:
        if explicit_method:
            raise
        selected_method = enforce_method(command.dish_title, '', command.ingredients, policy)
        facts['method'] = ''
    context = cooking_context(command.dish_title, selected_method, command.ingredients)
    facts['method'] = selected_method
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
        dish_identity=identity,
        intake_facts=facts,
    ).model_dump()
    say(state, f"אתה מכין {command.dish_title}. השלבים וההחלטות שלך; אפשר להוסיף פעולה או לדווח מה כבר עשית.")
    opening = [context["tips"][0]["text"]]
    if any(node["id"] == "fish_salmon_fillet" for node in context["graph"]["ingredients"]):
        opening = [
            PREP,
            "בחר איך להכין: מחבת לעור פריך, תנור להכנה בתבנית, או אידוי לתוצאה עדינה. לחץ על מסלול כדי להתחיל.",
        ]
    opening.extend(tip["text"] for tip in context["tips"] if tip["origin"] == "SAFETY_POLICY")
    say(state, "\n\n".join(dict.fromkeys(opening)))
    attach_recommendations(state, policy)
    refresh_decisions(state)
    guided_reply = guide_oven_salmon(state)
    if guided_reply:
        say(state, guided_reply)
    state["problem_options"] = options(
        state, problem_rules if problem_rules is not None else effective_rules()["rules"]
    )
    attach_intake(state)
    defaults = state['intake_guidance'].get('defaults')
    if defaults and not defaults.get('source_ids') and not state['custom_steps']:
        for title, instruction in [
            ('הכנה', 'הכן נתחי עוף מופשרים, תבנית תנור ותבלינים. ייבש את העוף בנייר מטבח.'),
            ('תיבול', 'מרח מעט שמן ותבל בתבלינים שבחרת. סדר בתבנית בשכבה אחת.'),
            ('צלייה בתנור', f"חמם ל־{defaults['temperature']}°C, {defaults['program']}. צלה כ־{defaults['minutes']} דקות ובדוק 74°C בחלק העבה."),
        ]:
            item = user_step(title, instruction, context)
            item['source'] = 'CHEF_DEFAULT:chicken_roast'
            state['custom_steps'].append(item)
        state['current_step'] = 0
    attach_operations(state)
    if state["intake_guidance"]["recipe_requested"] and not context["identified"] and not guided_reply:
        say(state, intake_reply(state))
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
    from app.ingredient_safety import check_ingredients
    if command.action not in {"update_plan", "finish", "pause", "timer_cancel"}:
        check_ingredients(
            [*state["ingredients"], *classification_ingredients(state.get("intake_facts", {}))],
            state["allergies"], state.get("forbid_meat_dairy", True),
        )
    previous_method_value = state["method"]
    # Re-derive safety/context from reported ingredients, not client-provided advice fields.
    classification = classification_ingredients(state.get("intake_facts", {}))
    context = cooking_context(state["dish_title"], state["method"], [*state["ingredients"], *classification])
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
    elif command.action == 'attach_recipe':
        if command.recipe_snapshot is None:
            raise DomainError('INVALID_REQUEST','Recipe steps are required',422)
        recipe=command.recipe_snapshot.model_dump()
        check_ingredients([*state["ingredients"], *recipe["ingredients"]], state["allergies"], state.get("forbid_meat_dairy", True))
        state['recipe_snapshot']=recipe
        state['custom_steps']=[user_step(f"שלב {index+1}",item['text'],state['context'],step_id=item['id']) for index,item in enumerate(recipe['steps'])]
        for entry in state['custom_steps']:entry['source']='USER_RECIPE_REFERENCE:'+recipe['id']
        state['current_step']=0;state['completed_step_ids']=[];state['stage_valid']=False
        state['intake_facts']['recipe_url']=recipe['url']
        say(state,'המתכון צורף: '+recipe['title']+'. שלב ראשון: '+recipe['steps'][0]['text'])
    elif command.action == "intake":
        if command.intake_facts is None:
            raise DomainError("INVALID_REQUEST", "Dish details are required", 422)
        facts = command.intake_facts.model_dump()
        if facts["family"] != "meat" and facts["protein"]:
            raise DomainError("INVALID_REQUEST", "A meat subtype requires the meat family", 422)
        classification = classification_ingredients(facts)
        check_ingredients([*state["ingredients"], *classification], state["allergies"], state.get("forbid_meat_dairy", True))
        requested_method = facts["method"] if "method" in command.intake_facts.model_fields_set else state["method"]
        selected_method = enforce_method(state["dish_title"], requested_method, [*state["ingredients"], *classification], policy)
        if facts != state.get("intake_facts"):
            state["measured_temperature"] = None
            state["measured_rest_seconds"] = None
            state["selected_operation_id"] = ""
        state["intake_facts"] = facts
        state["method"] = selected_method
        state["context"] = cooking_context(state["dish_title"], state["method"], [*state["ingredients"], *classification])
        state["context"]["graph"] = dietary_paths(state["context"]["graph"], state["allergies"], state["forbid_meat_dairy"])
        attach_intake(state)
        say(state, intake_reply(state))
    elif command.action == "select_operation":
        say(state, select_operation(state, command.operation_id))
    elif command.action == "request_operation":
        if not command.step_title.strip():
            raise DomainError("INVALID_REQUEST", "Name the missing operation", 422)
        state["operation_gaps"] = (state.get("operation_gaps", []) + [{"title": command.step_title.strip(), "details": command.message, "at": now, "status": "MISSING_RULE"}])[-30:]
        say(state, "חסרה פעולה במאגר: " + command.step_title.strip(), "user")
        say(state, "הפעולה נשמרה כחומר שחסר במאגר. כדי להוסיף לה הדרכה צריך: חומר גלם וכמות, כלי ושיטת עבודה, הוראות הפעולה, סימן הצלחה, תקלות אפשריות ומקור למתכון או לטכניקה. אפשר להביא את המידע דרך פרטי המנה.")
    elif command.action == "report_operation":
        reply = report_operation(state, command.operation_id, command.outcome_id, now)
        selected = BY_ID[command.operation_id]
        outcome = next(item for item in selected["outcomes"] if item["id"] == command.outcome_id)
        say(state, selected["label"] + ": " + outcome["label"], "user")
        say(state, reply)
        state["learning_focus"] = {"title": "לפי הפעולה והמצב שבחרת", "text": reply, "source": "", "origin": "STRUCTURED_OPERATION"}
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
        check_ingredients(command.ingredients, state["allergies"], command.forbid_meat_dairy)
        selected_method = enforce_method(command.dish_title, command.method, command.ingredients, policy)
        state["dish_title"], state["method"], state["ingredients"] = (
            command.dish_title,
            selected_method,
            command.ingredients,
        )
        state["context"] = cooking_context(command.dish_title, selected_method, command.ingredients)
        state["forbid_meat_dairy"] = command.forbid_meat_dairy
        state["context"]["graph"] = dietary_paths(
            state["context"]["graph"], state["allergies"], command.forbid_meat_dairy
        )
        state["measured_rest_seconds"] = None
        state["measured_temperature"] = None
        state["learning_focus"] = None
        state["decision_answers"] = {}
        state["intake_facts"] = {}
        state["selected_operation_id"] = ""
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
        state["method"] = path["method_ref"]
        if path["id"] == "salmon_oven_roast" and not steps:
            state["context"] = cooking_context(state["dish_title"], state["method"], state["ingredients"])
            state["context"]["graph"] = dietary_paths(
                state["context"]["graph"], state["allergies"], state["forbid_meat_dairy"]
            )
            say(state, guide_oven_salmon(state))
            attach_recommendations(state, policy)
            refresh_decisions(state)
            attach_intake(state)
            attach_operations(state)
            state["revision"] += 1
            state["last_user_at"] = now
            return state
        state["decision_answers"]["progress"] = "not_started"
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
        say(state, steps[state["current_step"]]["instruction"])
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
        if is_oven_salmon(state) and not current:
            say(state, guide_oven_salmon(state))
        elif (
            is_oven_salmon(state)
            and current
            and current["title"] == "אפייה ובדיקת המרכז"
            and (state["measured_temperature"] is None or state["measured_temperature"] < 63)
        ):
            say(
                state,
                "לפני ההגשה, מדוד במרכז החלק העבה ודווח את המדידה בכפתור מדידת הטמפרטורה. נדרשת מדידה של 63°C לפחות; אם נמוכה יותר, המשך לאפות ובדוק שוב.",
            )
        elif not current:
            say(state, "אפשר להוסיף פעולה משלך, או פשוט לדווח מה עשית. אין צורך להשלים תסריט של המערכת.")
        else:
            if current["id"] not in state["completed_step_ids"]:
                state["completed_step_ids"].append(current["id"])
            next_index = next(
                (i for i, item in enumerate(steps) if item["id"] not in state["completed_step_ids"]), None
            )
            if next_index is not None:
                state["current_step"] = next_index
                if is_oven_salmon(state) and steps[next_index]["title"] == "אפייה ובדיקת המרכז":
                    state["measured_temperature"] = None
            say(
                state,
                steps[next_index]["instruction"]
                if next_index is not None
                else "סיימת את פעולות המסלול לפי דיווחך. אפשר לבדוק תיבול, לבקש עזרה או לסיים את הבישול. השלמת פעולות אינה אישור בטיחות.",
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
            guided_reply = guide_oven_salmon(state)
            if guided_reply:
                reply = guided_reply
            if (
                not is_oven_salmon(state)
                and state["decision_answers"].get("progress") == "not_started"
                and not steps
                and any(node["id"] == "fish_salmon_fillet" for node in context["graph"]["ingredients"])
            ):
                reply = PREP + "\n\nבחר מסלול הכנה למטה כדי לקבל הוראות צעד אחר צעד."
            state["learning_focus"] = {"title": label or "בחירת אפשרות", "text": reply, "source": ""}
            say(state, reply)
            state["context"] = cooking_context(state["dish_title"], state["method"], state["ingredients"])
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
            specific_reply = report_guidance(state, text)
            reply, issue = contextual_reply(
                context, text, current["title"] if current else "", state["mode"] == "consultant"
            )
            if (
                not issue
                and current
                and current["source"].startswith(("USER_GRAPH_ADAPTED:", "CHEF_AUTHORED:"))
            ):
                reply = current["instruction"] + " " + current["chefQuestions"][0]
                if text in ("מה לבדוק לפני שממשיכים?", "בדוק את ההתקדמות שלי", "המנה נראית טוב"):
                    reply = "לפני המשך: " + " · ".join(current["successCriteria"])
                elif text == "איך לתבל ולהגיש?":
                    reply = "העבר לכלי נקי. טעם והוסף מעט מלח, לימון או שמן זית לפי הטעם, בכל פעם מעט. בדיקת תיבול אינה מחליפה בדיקת מוכנות."
            if specific_reply:
                reply, issue = specific_reply, ""
            elif command.action == "ask" and not issue:
                query_tips = practical_dish_tips(context, " ".join([state["dish_title"], *state["ingredients"], text]))
                from app.method_policy import canonical_method
                from app.practical_knowledge import step_guidance

                if current and text in ("איך לבצע את הפעולה הנוכחית?", "מה לבדוק לפני שממשיכים?"):
                    scoped = step_guidance(
                        state["dish_title"], canonical_method(state["method"]),
                        current["title"] + " " + current["instruction"],
                        checks=text == "מה לבדוק לפני שממשיכים?",
                    )
                    if scoped:
                        query_tips.insert(0, scoped)
                if not query_tips and any(term in text for term in ("חרדל", "ויניגרט", "קקאו", "שוקולד", "mustard", "vinaigrette", "cocoa", "chocolate")):
                    query_tips = book_tips(text)
                book_tip = next((tip for tip in query_tips if tip.get("practical")), None)
                if not book_tip:
                    book_tip = next((tip for tip in query_tips if tip["source_ids"][1].startswith(("EVD-MCG-RNG-", "RUL-MCG-RNG-"))), None)
                if not book_tip:
                    book_tip = next((tip for tip in query_tips if tip["origin"] == "OBSIDIAN_FOODLAB"), None)
                if book_tip:
                    reply += "\n\n" + book_tip["text"]
            if command.action == "report":
                reply = "הדיווח התקבל: " + text[:240] + "\n\n" + reply
            state["learning_focus"] = {"title": issue or "בהקשר לדיווח האחרון", "text": reply, "source": ""}
            if specific_reply:
                state["learning_focus"].update(origin="USER_SUPPLIED_PROTOCOL", source_ids=["USER_GIZZARD_PROTOCOL_2026_10_25"])
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
    if command.action == "update_plan":
        guided_reply = guide_oven_salmon(state)
        if guided_reply:
            say(state, guided_reply)
    attach_recommendations(state, policy)
    refresh_decisions(state)
    if command.action in ("answer", "report", "ask", "check_in") and not steps and not state["decision_questions"] and state["method"]:
        if (state["context"]["graph"].get("method") or {}).get("id") == "boil_simmer" and state["decision_answers"].get("condition") in ("fresh_clean", "thawed_clean"):
            if any(node["id"] == "chicken_giblets" for node in state["context"]["graph"]["ingredients"]):
                for title, instruction in [
                    ("הכנת הסיר", preparation_guidance()),
                    ("בישול בבעבוע עדין", "לאחר הרתיחה הנמך לבעבוע עדין. בדוק מדי פעם את מפלס הנוזל ואת הרכות; משך הבישול תלוי בגודל ובכמות."),
                    ("בדיקת רכות ומוכנות", "בדוק רכות בנפרד מבטיחות. מדוד בחלקים העבים וודא עמידה בסף 74°C לעוף לפני ההגשה; רתיחת הנוזל אינה מדידת ליבה."),
                ]:
                    entry = user_step(title, instruction, state["context"])
                    entry["source"] = "CHEF_AUTHORED:gizzard_simmer"
                    entry["successCriteria"] = {
                        "הכנת הסיר": ["הקורקבנים מופשרים ונקיים", "הנוזל כמעט עד גובה הקורקבנים", "לאחר הרתיחה הונמכה האש לבעבוע עדין"],
                        "בישול בבעבוע עדין": ["בועות קטנות עולות בעדינות, בלי רתיחה סוערת", "יש נוזל והתחתית אינה נחרכת", "בדוק חתיכה במזלג ודווח אם עדיין קשה או כבר רכה"],
                        "בדיקת רכות ומוכנות": ["המזלג נכנס בקלות לחתיכה", "נמדדו לפחות 74°C בחלקים העבים לפני הגשה"],
                    }[title]
                    steps.append(entry)
                if command.action in ("answer", "check_in"):
                    choice = "הבחירות נשמרו. בחרת תבשיל רך ברוטב." if state["decision_answers"].get("goal") == "sauce" else "הבחירות נשמרו."
                    say(state, choice + "\n\n" + steps[0]["instruction"])
        paths = [path for path in state["context"]["graph"]["paths"]
                 if path["selectable"] and path["method_ref"] == (state["context"]["graph"].get("method") or {}).get("id")]
        if not steps and len(paths) == 1 and command.action == "answer" and not state["safety_hold"]:
            return apply_user_command(state, command.model_copy(update={"action": "adopt_path", "graph_path_id": paths[0]["id"]}), now, problem_rules, method_policy)
    enrich_context(state["context"], " ".join([state["dish_title"], state["method"], command.message, *state["ingredients"]]))
    from app.culinary_context import strict_context
    strict_context(state['context'], state['dish_title'], [*state['ingredients'], *classification_ingredients(state.get('intake_facts', {}))])
    attach_intake(state)
    defaults = state['intake_guidance'].get('defaults')
    if defaults and not defaults.get('source_ids'):
        for item in steps:
            if item.get('source') == 'CHEF_DEFAULT:chicken_roast' and item['title'] == 'צלייה בתנור':
                item['instruction'] = f"חמם ל־{defaults['temperature']}°C, {defaults['program']}. צלה כ־{defaults['minutes']} דקות ובדוק 74°C בחלק העבה."
    attach_operations(state)
    from app.station_protocol import attach_station

    attach_station(state)
    state["revision"] += 1
    return state
