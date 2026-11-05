"""Authored starter guidance; technique examples are not kitchen-tested recipes."""

from app.knowledge_graph import GraphPath

SAFETY_SOURCE = (
    "https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-fresh-and-frozen-seafood-safely"
)
PREP = "הכן פילה סלמון מופשר ושמור בקירור עד ההכנה. בדוק והסר עצמות, יבש בעדינות בנייר סופג ותבל במלח ופלפל לפי הטעם. הכן כלי נקי להגשה ומדחום מזון. אם הוא קפוא, הפשר במקרר לפני המסלול הזה."
RECIPE_SOURCE = "https://www.bbcgoodfood.com/recipes/baked-salmon"


def is_oven_salmon(state):
    context = state.get("context") or {}
    graph = context.get("graph") or {}
    return (graph.get("method") or {}).get("id") == "oven_roast" and any(
        node["id"] == "fish_salmon_fillet" for node in graph.get("ingredients", [])
    )


def oven_questions(state):
    if not is_oven_salmon(state) or state["custom_steps"]:
        return None

    def choices(*pairs):
        return [(key, label, [], "בחרת: " + label + ".", "") for key, label in pairs]

    return [
        (
            "salmon_condition",
            "הסלמון מופשר או עדיין קפוא?",
            choices(("thawed", "טרי או מופשר לגמרי"), ("frozen", "עדיין קפוא — נתחיל בהפשרה")),
        ),
        (
            "salmon_cut",
            "מה גודל הנתח?",
            choices(("fillets", "מנות פילה אישיות"), ("side", "נתח פילה גדול — לא דג שלם")),
        ),
        (
            "salmon_thickness",
            "מה העובי בחלק העבה?",
            choices(
                ("thin", "עד כ־2 ס״מ"), ("thick", "יותר מ־2 ס״מ"), ("unknown", "לא בטוח — אבדוק במהלך האפייה")
            ),
        ),
        (
            "salmon_style",
            "איזו תוצאה תרצה?",
            choices(("open", "אפייה פתוחה — מעט השחמה"), ("covered", "אפייה מכוסה — תוצאה עדינה")),
        ),
        (
            "salmon_flavor",
            "איזה תיבול תרצה?",
            choices(
                ("lemon", "לימון ושמן זית"), ("herbs", "שום ועשבי תיבול"), ("plain", "עדין — מלח ושמן זית")
            ),
        ),
    ]


def guide_oven_salmon(state):
    """Start the authored plan after explicit preferences, without a second start click."""
    if not is_oven_salmon(state):
        return None
    state["guidance_links"] = [
        {"title": "מתכון מצולם לסלמון בתנור — Good Food (אנגלית)", "url": RECIPE_SOURCE},
        {"title": "הפשרה ובדיקת מוכנות דגים — FDA (אנגלית)", "url": SAFETY_SOURCE},
    ]
    questions = oven_questions(state)
    if questions is None:
        return None
    answers = state["decision_answers"]
    missing = [q for q in questions if answers.get(q[0]) not in {option[0] for option in q[2]}]
    if missing:
        return "נכין סלמון בתנור יחד. אבחר עבורך סדר עבודה ברור לפי התשובות שלך.\n\n" + missing[0][1]
    from app.consultant import user_step

    flavor = answers["salmon_flavor"]
    seasoning = {
        "lemon": "לכל מנת פילה של כ־200 גרם ערבב כפית שמן זית עם כפית מיץ לימון וקורט מלח; מרח על פני הדג. אפשר להוסיף פלפל לפי הטעם.",
        "herbs": "לכל מנת פילה של כ־200 גרם ערבב כפית שמן זית, חצי שן שום כתושה, כפית פטרוזיליה או שמיר קצוצים וקורט מלח. מרח על פני הדג.",
        "plain": "לכל מנת פילה של כ־200 גרם מרח כפית שמן זית ופזר קורט מלח. אין צורך במרינדה או בהמתנה לפני האפייה.",
    }[flavor]
    portion = (
        "הנח את המנות בשכבה אחת עם רווח קטן ביניהן."
        if answers["salmon_cut"] == "fillets"
        else "הנח את הנתח הגדול בשלמותו בתבנית שמכילה אותו בלי קיפול. מדוד בהמשך בכמה מקומות עבים, לא רק בקצה הדק."
    )
    thickness = (
        "הנתח דק: בדוק מוקדם ולעיתים קרובות, כדי לא לייבש אותו."
        if answers["salmon_thickness"] == "thin"
        else "החלק העבה מכתיב את קצב הבישול; אל תסתמך על השוליים הדקים."
    )
    covering = (
        "כסה את התבנית באופן רופף בנייר אלומיניום; פתח בהמשך בזהירות מהאדים."
        if answers["salmon_style"] == "covered"
        else "השאר את התבנית ללא כיסוי כדי לאפשר מעט השחמה על פני הדג."
    )
    timing = (
        "במתכון המקושר טווח האפייה למנות פילה הוא כ־10–15 דקות; זה אומדן לתכנון ובדיקה, ולא אישור מוכנות. "
        if answers["salmon_cut"] == "fillets"
        else "לנתח גדול אין כאן זמן סיום קבוע; בדוק בכמה מקומות עבים. "
    )
    steps = []
    if answers["salmon_condition"] == "frozen":
        steps.append(
            (
                "הפשרה במקרר",
                "הנח את הדג בכלי במקרר והפשר עד שאין מרכז קפוא. אם הוא ארוז בוואקום, פעל לפי הוראות ההפשרה שעל האריזה. אל תפשיר על השיש. חזור לכאן ולחץ על המשך רק אחרי שהופשר.",
                "הדג מופשר לגמרי ונשמר קר",
            )
        )
    steps.extend(
        [
            (
                "חימום התנור והכנת התבנית",
                "חמם תנור ל־180°C בחום עליון ותחתון, או 160°C בטורבו. מקם רשת במרכז התנור. רפד תבנית בנייר אפייה המתאים לטמפרטורה והכן מדחום, נייר סופג וכלי נקי להגשה. שמור את הדג בקירור בזמן החימום.",
                "התנור הגיע לטמפרטורה והתבנית מוכנה",
            ),
            (
                "בדיקת עצמות ותיבול",
                "הוצא את הדג, העבר אצבע בעדינות לאורך מרכז הפילה והוצא עצמות מורגשות בפינצטה נקייה. ספוג לחות בנייר סופג. "
                + seasoning
                + " "
                + portion
                + " אם יש עור, הנח אותו כלפי מטה; אין צורך להסירו.",
                "הדג נבדק לעצמות, יובש, תובל והונח בתבנית",
            ),
            (
                "אפייה ובדיקת המרכז",
                "הכנס את התבנית למדף המרכזי בתנור החם. "
                + covering
                + " אין צורך להפוך. "
                + timing
                + thickness
                + " החדר מדחום מהצד אל מרכז החלק העבה, בלי לגעת בתבנית. יעד הבדיקה הוא 63°C. אם המדידה נמוכה, החזר לתנור ובדוק שוב; הזמן תלוי בעובי ובתנור.",
                "נמדדו לפחות 63°C בחלקים העבים; צבע חיצוני לבדו אינו מספיק",
            ),
            (
                "הגשה",
                "לאחר בדיקת המוכנות הוצא את התבנית בכפפות והעבר את הדג במרית רחבה לכלי נקי. טעם חתיכה מבושלת והוסף מעט לימון או מלח לפי הטעם. אפשר להגיש לצד אורז, ירקות או סלט.",
                "הדג הועבר לכלי נקי והתיבול מתאים",
            ),
        ]
    )
    for index, (title, instruction, checkpoint) in enumerate(steps):
        item = user_step(title, instruction, state["context"])
        item.update(
            source="CHEF_AUTHORED:salmon/oven/" + str(index),
            why="סדר עבודה מותאם לבחירות שלך; בדיקת הבטיחות מבוססת על הנחיות FDA.",
            successCriteria=[checkpoint],
            chefQuestions=["האם " + checkpoint + "?"],
            commonMistakes=["אל תסתמך על זמן בלבד לבדיקת מוכנות."],
            next_step_prep=steps[index + 1][0] if index + 1 < len(steps) else "סיום והגשה",
        )
        state["custom_steps"].append(item)
    state["current_step"] = 0
    state["learning_focus"] = None
    return state["custom_steps"][0]["instruction"]


def add_salmon_paths(context):
    if not any(node["id"] == "fish_salmon_fillet" for node in context["graph"]["ingredients"]):
        return context
    selected = context["graph"].get("method")
    variants = [
        (
            "oven_roast",
            "סלמון בתנור",
            [
                ("הכנת הסלמון", PREP, "הפילה מופשר, ללא עצמות מורגשות ומתובל"),
                (
                    "הכנת התבנית",
                    "חמם תנור ל־180°C. הנח את הסלמון בתבנית משומנת קלות, כשהעור כלפי מטה אם יש עור. אפשר להוסיף לימון ושמן זית לפי הטעם.",
                    "התנור חם והפילה מונח בשכבה אחת",
                ),
                (
                    "אפייה ובדיקה",
                    "הכנס לתנור. בדוק במרכז החלק העבה בעזרת מדחום מזון; המשך לאפות ולבדוק עד 63°C. העובי והתנור משפיעים על המשך, לכן אל תקבע מוכנות לפי זמן בלבד.",
                    "נמדדו לפחות 63°C בחלקים העבים",
                ),
                (
                    "הגשה",
                    "העבר לכלי נקי. טעם והתאם לימון ותיבול לפני ההגשה.",
                    "הדג הועבר לכלי נקי והתיבול מתאים",
                ),
            ],
        ),
        (
            "steam",
            "סלמון באידוי",
            [
                ("הכנת הסלמון", PREP, "הפילה מופשר, ללא עצמות מורגשות ומתובל"),
                (
                    "הכנת כלי האידוי",
                    "הוסף מים לסיר מתחת לגובה סלסילת האידוי והבא לבעבוע. הנח את הסלמון בסלסילה משומנת קלות בלי שהמים ייגעו בו, וסגור מכסה.",
                    "יש אדים, המכסה סגור והדג אינו שקוע במים",
                ),
                (
                    "אידוי ובדיקה",
                    "שמור על יצירת אדים וודא שהמים אינם מתאדים לגמרי. פתח בזהירות הרחק מהפנים ומדוד בחלק העבה; המשך לאדות ולבדוק עד 63°C.",
                    "נמדדו לפחות 63°C בחלקים העבים",
                ),
                (
                    "הגשה",
                    "העבר בעדינות לכלי נקי והוסף לימון ותיבול לפי הטעם.",
                    "הדג הועבר לכלי נקי והתיבול מתאים",
                ),
            ],
        ),
    ]
    for method, title, steps in variants:
        if selected and selected["id"] != method:
            continue
        details = [
            {
                "title": name,
                "instruction": instruction,
                "successCriteria": [checkpoint],
                "chefQuestions": ["מה המצב? " + checkpoint],
                "source_id": "editorial/salmon/" + method + "/" + str(index),
            }
            for index, (name, instruction, checkpoint) in enumerate(steps)
        ]
        context["graph"]["paths"].append(
            GraphPath(
                id="salmon_" + method,
                title=title,
                ingredient_ref="fish_salmon_fillet",
                method_ref=method,
                suggestions=[item[0] for item in steps],
                selectable=True,
                source_id="editorial/salmon/" + method,
                domain_source_id=SAFETY_SOURCE,
                detailed_steps=details,
            ).model_dump()
        )
    return context
