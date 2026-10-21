"""Editable, reviewer-approved replies; absent rules are explicit, never invented."""

from pathlib import Path

from fastapi import Depends
from pydantic import Field, ValidationError, model_validator
from sqlalchemy import select

from app.db import CulinarySourceRevision
from app.knowledge import DomainError, audit
from app.schemas import StrictModel

SOURCE = Path(__file__).with_name("data") / "problem_rules.yaml"
LABELS = {
    "burning": "נשרף או מתחיל להיחרך",
    "sticking": "נדבק לכלי",
    "too_thick": "רוטב סמיך מדי",
    "too_thin": "רוטב דליל מדי",
    "too_salty": "מלוח מדי",
    "too_dry": "יבש מדי",
    "tough": "עדיין קשה ולא מתרכך",
    "other": "בעיה אחרת",
    "fire": "סיכון אש או להבה לא נשלטת",
}
ALIASES = {
    "שרוף": "burning",
    "נשרף": "burning",
    "נדבק": "sticking",
    "סמיך מדי": "too_thick",
    "דליל מדי": "too_thin",
    "מלוח מדי": "too_salty",
    "יבש מדי": "too_dry",
    "לא מתרכך": "tough",
    "קשה מדי": "tough",
}


class ProblemVariant(StrictModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]{0,59}$")
    response: str = Field(min_length=8, max_length=2000)
    methods: list[str] = Field(default_factory=list, max_length=20)
    families: list[str] = Field(default_factory=list, max_length=20)
    ingredient_ids: list[str] = Field(default_factory=list, max_length=40)
    dish_terms: list[str] = Field(default_factory=list, max_length=40)
    stages: list[str] = Field(default_factory=list, max_length=8)
    answers: dict[str, str] = Field(default_factory=dict, max_length=8)
    sources: list[str] = Field(default_factory=list, max_length=8)


class ProblemOption(StrictModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]{0,39}$")
    label: str = Field(min_length=1, max_length=160)


class ProblemQuestion(StrictModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]{0,39}$")
    text: str = Field(min_length=1, max_length=300)
    options: list[ProblemOption] = Field(min_length=2, max_length=8)


class ProblemRule(StrictModel):
    response: str = Field(default="", max_length=2000)
    methods: list[str] = Field(default_factory=list, max_length=20)
    questions: list[ProblemQuestion] = Field(default_factory=list, max_length=4)
    variants: list[ProblemVariant] = Field(default_factory=list, max_length=40)

    @model_validator(mode="after")
    def references(self):
        questions = {q.id: q for q in self.questions}
        if len(questions) != len(self.questions) or len({v.id for v in self.variants}) != len(self.variants):
            raise ValueError("Duplicate question or variant IDs")
        if not self.response.strip() and not self.variants:
            raise ValueError("A response or contextual variants are required")
        if self.response and len(self.response.strip()) < 8:
            raise ValueError("Response must contain at least eight characters")
        for question in self.questions:
            if len({option.id for option in question.options}) != len(question.options):
                raise ValueError("Duplicate option IDs")
        for variant in self.variants:
            for key, answer in variant.answers.items():
                if key not in questions or answer not in {o.id for o in questions[key].options}:
                    raise ValueError("Unknown question or option reference")
        return self


class RuleBook(StrictModel):
    rules: dict[str, ProblemRule] = Field(max_length=30)


class RuleUpdate(StrictModel):
    expected_revision: int = Field(ge=0)
    yaml_text: str = Field(min_length=1, max_length=32768)
    reviewed: bool


class RuleDraft(StrictModel):
    yaml_text: str = Field(min_length=1, max_length=32768)


def parse_rules(text):
    # Reuse the bounded safe YAML parser, including duplicate/recursive-key checks.
    from app.culinary_sources import parse

    try:
        book = RuleBook.model_validate(parse(text))
        if any(key not in LABELS or key == "fire" for key in book.rules):
            raise ValueError("Use a listed problem id; fire policy cannot be overridden")
        from app.culinary_context import FAMILIES
        from app.knowledge_graph import graph
        from app.method_policy import canonical_method

        families = {entry[0] for entry in FAMILIES} | {"unknown"}
        ingredient_ids = set(graph()["ingredients"])
        for rule in book.rules.values():
            for methods in [rule.methods, *(variant.methods for variant in rule.variants)]:
                if any(canonical_method(value) is None for value in methods):
                    raise ValueError("Unknown method selector")
            for variant in rule.variants:
                if not set(variant.families) <= families or not set(variant.ingredient_ids) <= ingredient_ids:
                    raise ValueError("Unknown family or ingredient selector")
                if not set(variant.stages) <= {"not_started", "cooking", "finishing"}:
                    raise ValueError("Unknown progress selector")
        return book.model_dump()["rules"]
    except (ValidationError, ValueError) as exc:
        raise DomainError(
            "INVALID_RULES", "Check problem IDs, selectors, questions, options and responses", 422
        ) from exc


def effective_rules(session=None, owner=None):
    row = None
    if session is not None:
        row = session.scalar(
            select(CulinarySourceRevision)
            .where(
                CulinarySourceRevision.owner_id == owner,
                CulinarySourceRevision.source_key == "problem_rules",
            )
            .order_by(CulinarySourceRevision.number.desc())
            .limit(1)
        )
    text = row.yaml_text if row else SOURCE.read_text(encoding="utf-8")
    return {"revision": row.number if row else 0, "yaml_text": text, "rules": parse_rules(text)}


def options(state, rules):
    return [
        {
            "id": key,
            "label": label,
            "rule_available": key == "fire"
            or (
                key in rules
                and method_matches(state["method"], rules[key].get("methods", []))
                and (
                    bool(rules[key].get("response"))
                    or any(matches_context(state, variant) for variant in rules[key].get("variants", []))
                )
            ),
        }
        for key, label in LABELS.items()
    ]


def identify_problem(command):
    if command.problem_id:
        if command.problem_id not in LABELS:
            raise DomainError("INVALID_PROBLEM", "Choose a listed problem", 422)
        return command.problem_id
    text = command.message.strip().rstrip(".!?")
    match = next((key for key, label in LABELS.items() if text == label), None)
    return match or ALIASES.get(text, "")


def method_matches(method, allowed):
    from app.method_policy import canonical_method

    return (
        not allowed
        or method in allowed
        or (
            canonical_method(method) is not None
            and canonical_method(method) in {canonical_method(value) for value in allowed}
        )
    )


def matches_context(state, variant):
    from app.knowledge_graph import phrase_spans

    context = state["context"]
    nodes = {node["id"] for node in context["graph"]["ingredients"]}
    return (
        method_matches(state["method"], variant.get("methods", []))
        and (not variant.get("families") or context["family"] in variant["families"])
        and (not variant.get("ingredient_ids") or bool(nodes.intersection(variant["ingredient_ids"])))
        and (
            not variant.get("dish_terms")
            or bool(
                phrase_spans(
                    " ".join([state["dish_title"], *state["ingredients"]]).casefold(), variant["dish_terms"]
                )
            )
        )
        and (
            not variant.get("stages")
            or state.get("decision_answers", {}).get("progress") in variant["stages"]
        )
    )


def problem_reply(state, key, description, rules, answers=None):
    state["problem_questions"] = []
    state["problem_rule_match"] = {}
    state["pending_problem"] = {}
    rule = rules.get(key)
    answers = answers or {}
    if rule and method_matches(state["method"], rule.get("methods", [])):
        variants = [
            v
            for v in rule.get("variants", [])
            if matches_context(state, v)
            and all(
                name not in answers or answers[name] == value for name, value in v.get("answers", {}).items()
            )
        ]
        # Ask only questions used by candidate rules, in source order.
        required = {name for v in variants for name in v.get("answers", {})}
        unanswered = [q for q in rule.get("questions", []) if q["id"] in required and q["id"] not in answers]
        if unanswered:
            question = unanswered[0]
            state["problem_rule_status"] = "clarify"
            state["pending_problem"] = {"problem_id": key, "description": description, "answers": answers}
            state["problem_questions"] = [
                {
                    "id": "problem_" + question["id"],
                    "text": question["text"],
                    "options": [
                        dict(option, number=index + 1) for index, option in enumerate(question["options"])
                    ],
                }
            ]
            return f"כדי להתאים טיפול לבעיה ״{LABELS[key]}״, בחר את המצב שמתאים למנה."
        for variant in variants:
            if all(answers.get(name) == value for name, value in variant.get("answers", {}).items()):
                state["problem_rule_status"] = "matched"
                state["problem_rule_match"] = {
                    "problem_id": key,
                    "variant_id": variant["id"],
                    "answers": answers,
                    "sources": variant.get("sources", []),
                }
                return variant["response"]
        if rule.get("response", "").strip():
            state["problem_rule_status"] = "matched"
            state["problem_rule_match"] = {"problem_id": key, "variant_id": "fallback", "answers": answers}
            return rule["response"]
    state["problem_rule_status"] = "missing"
    missing = {
        "problem_id": key,
        "method": state["method"],
        "description": description[:2000],
        "dish_title": state["dish_title"],
        "family": state["context"]["family"],
        "ingredient_ids": [node["id"] for node in state["context"]["graph"]["ingredients"]],
        "stage": state.get("decision_answers", {}).get("progress", "unknown"),
        "answers": answers,
    }
    backlog = state.setdefault("missing_problem_rules", [])
    if missing not in backlog:
        state["missing_problem_rules"] = (backlog + [missing])[-30:]
    return (
        f"חסר חוק תגובה מתאים לבעיה ״{LABELS[key]}״ (מזהה: {key}). "
        "הבעיה נשמרה ברשימת החוקים החסרים. אפשר להוסיף חוק במאגר הידע, תחת כללי טיפול בבעיות. "
        "לא ניתנה הנחיית טיפול אוטומטית בלי חוק מתאים."
    )


def accept_problem_choice(state, command, rules):
    pending = state.get("pending_problem", {})
    rule = rules.get(pending.get("problem_id"), {})
    question = next(
        (q for q in rule.get("questions", []) if "problem_" + q["id"] == command.question_id), None
    )
    current = any(q["id"] == command.question_id for q in state.get("problem_questions", []))
    if (
        not pending
        or not current
        or not question
        or command.answer not in {o["id"] for o in question["options"]}
    ):
        raise DomainError("INVALID_CHOICE", "Choose a current problem option", 422)
    label = next(o["label"] for o in question["options"] if o["id"] == command.answer)
    answers = dict(pending["answers"], **{command.question_id.removeprefix("problem_"): command.answer})
    return problem_reply(state, pending["problem_id"], pending["description"], rules, answers), label


def install_problem_routes(app, db, principal, reviewer):
    @app.get("/v1/coach/problem-rules/template")
    def template():
        return {**effective_rules(), "problem_ids": LABELS}

    @app.get("/v1/coach/problem-rules")
    def read(session=Depends(db), owner=Depends(principal)):
        return {**effective_rules(session, owner.user_id), "problem_ids": LABELS}

    @app.post("/v1/coach/problem-rules/with-defaults")
    def preview_defaults(body: RuleDraft, owner=Depends(reviewer)):
        import yaml

        draft = parse_rules(body.yaml_text)
        defaults = effective_rules()["rules"]
        added = [key for key in defaults if key not in draft]
        merged = {**defaults, **draft}
        return {
            "yaml_text": yaml.safe_dump({"rules": merged}, allow_unicode=True, sort_keys=False),
            "added_ids": added,
        }

    @app.put("/v1/coach/problem-rules")
    def save(body: RuleUpdate, session=Depends(db), owner=Depends(reviewer)):
        if not body.reviewed:
            raise DomainError("REVIEW_REQUIRED", "Review the responses before activating them", 422)
        parse_rules(body.yaml_text)
        previous = effective_rules(session, owner.user_id)
        if previous["revision"] != body.expected_revision:
            raise DomainError("SOURCE_CONFLICT", "Rules changed; reload before saving", 409)
        session.add(
            CulinarySourceRevision(
                owner_id=owner.user_id,
                source_key="problem_rules",
                number=body.expected_revision + 1,
                yaml_text=body.yaml_text,
            )
        )
        audit(session, owner.user_id, "problem_rules_reviewed", revision=body.expected_revision + 1)
        session.commit()
        return {**effective_rules(session, owner.user_id), "problem_ids": LABELS}
