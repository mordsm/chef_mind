"""Configurable method allowlists, enforced on server-side method changes."""

import re
from pathlib import Path

from fastapi import Depends
from pydantic import Field, ValidationError, model_validator
from sqlalchemy import select

from app.culinary_context import dish_context
from app.db import CulinarySourceRevision
from app.knowledge import DomainError, audit
from app.knowledge_graph import METHODS, match_method, phrase_spans
from app.problem_rules import RuleUpdate
from app.schemas import StrictModel

SOURCE = Path(__file__).with_name("data") / "method_policy.yaml"
METHOD_LABELS = {key: entry[0] for key, entry in METHODS.items()} | {"pressure": "סיר לחץ"}


class MethodProfile(StrictModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]{0,79}$")
    title: str = Field(min_length=1, max_length=160)
    ingredient_ids: list[str] = Field(default_factory=list, max_length=80)
    title_terms: list[str] = Field(default_factory=list, max_length=40)
    family: str = Field(default="", max_length=40)
    allowed: list[str] = Field(max_length=20)
    reason: str = Field(min_length=8, max_length=1000)
    blocked_reasons: dict[str, str] = Field(default_factory=dict, max_length=20)

    @model_validator(mode="after")
    def valid_profile(self):
        if not (self.ingredient_ids or self.title_terms or self.family):
            raise ValueError("A profile must have a selector")
        if any(key not in METHOD_LABELS for key in [*self.allowed, *self.blocked_reasons]) or any(
            not reason.strip() for reason in self.blocked_reasons.values()
        ):
            raise ValueError("Unknown method or empty reason")
        return self


class MethodPolicy(StrictModel):
    default_reason: str = Field(min_length=8, max_length=1000)
    profiles: list[MethodProfile] = Field(max_length=150)


class MethodOptionsRequest(StrictModel):
    dish_title: str = Field(max_length=200)
    ingredients: list[str] = Field(default_factory=list, max_length=100)


def parse_policy(text):
    from app.culinary_sources import parse

    try:
        policy = MethodPolicy.model_validate(parse(text)).model_dump()
        ids = [profile["id"] for profile in policy["profiles"]]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate profile IDs")
        return policy
    except (ValueError, ValidationError) as exc:
        raise DomainError(
            "INVALID_METHOD_POLICY", "Check profile selectors, method IDs and explanations", 422
        ) from exc


def effective_policy(session=None, owner=None):
    row = None
    if session is not None:
        row = session.scalar(
            select(CulinarySourceRevision)
            .where(
                CulinarySourceRevision.owner_id == owner, CulinarySourceRevision.source_key == "method_policy"
            )
            .order_by(CulinarySourceRevision.number.desc())
            .limit(1)
        )
    text = row.yaml_text if row else SOURCE.read_text(encoding="utf-8")
    policy = parse_policy(text)
    if row is None:
        from app.culinary_engine_api import profiles

        policy["profiles"] = profiles(METHOD_LABELS) + policy["profiles"]
    return {
        "revision": row.number if row else 0,
        "yaml_text": text,
        "policy": policy,
        "methods": METHOD_LABELS,
    }


def recommendations(title, ingredients, policy, context=None):
    context = context or dish_context(title, "", ingredients)
    nodes = {node["id"] for node in context["graph"]["ingredients"]}
    text = " ".join([title, *ingredients]).casefold()
    profile = None
    for candidate in policy["profiles"]:
        if candidate["ingredient_ids"] and not nodes.intersection(candidate["ingredient_ids"]):
            continue
        if candidate["title_terms"] and not phrase_spans(text, candidate["title_terms"]):
            continue
        if candidate["family"] and candidate["family"] != context["family"]:
            continue
        profile = candidate
        break
    allowed = profile["allowed"] if profile else []
    reason = profile["reason"] if profile else policy["default_reason"]
    explanations = profile["blocked_reasons"] if profile else {}
    return {
        "profile_id": profile["id"] if profile else None,
        "profile_title": profile["title"] if profile else "אין פרופיל מתאים",
        "allowed": [{"id": key, "label": METHOD_LABELS[key]} for key in dict.fromkeys(allowed)],
        "blocked": [
            {"id": key, "label": label, "reason": explanations.get(key, reason)}
            for key, label in METHOD_LABELS.items()
            if key not in allowed
        ],
        "reason": reason,
    }


def canonical_method(value):
    if value in METHOD_LABELS:
        return value
    if value.strip() in ("סיר לחץ", "pressure cooker"):
        return "pressure"
    selected = match_method(value)
    return selected["id"] if selected else None


def enforce_method(title, method, ingredients, policy):
    title_without_negations = re.sub(r"(?:ללא|בלי|without)\s+\S+", "", title)
    selected = canonical_method(method) if method else canonical_method(title_without_negations)
    if not method and not selected:
        return ""
    allowed = recommendations(title, ingredients, policy)
    if selected not in {item["id"] for item in allowed["allowed"]}:
        blocked = next((item for item in allowed["blocked"] if item["id"] == selected), None)
        reason = blocked["reason"] if blocked else allowed["reason"]
        raise DomainError("METHOD_NOT_RECOMMENDED", METHOD_LABELS.get(selected, method) + ": " + reason, 422)
    return METHOD_LABELS[selected]


def attach_recommendations(state, policy):
    result = recommendations(state["dish_title"], state["ingredients"], policy, state["context"])
    state["method_recommendations"] = result
    selected = canonical_method(state["method"]) if state["method"] else None
    blocked = next((item for item in result["blocked"] if item["id"] == selected), None)
    state["method_warning"] = blocked["reason"] if blocked else ""
    for path in state["context"]["graph"]["paths"]:
        if path["method_ref"] not in {item["id"] for item in result["allowed"]}:
            path.update(selectable=False, reason=result["reason"])


def install_method_routes(app, db, principal, reviewer):
    @app.get("/v1/coach/method-policy/template")
    def template():
        return effective_policy()

    @app.get("/v1/coach/method-policy")
    def read(session=Depends(db), owner=Depends(principal)):
        return effective_policy(session, owner.user_id)

    @app.post("/v1/coach/method-policy/options")
    def public_options(body: MethodOptionsRequest):
        return recommendations(body.dish_title, body.ingredients, effective_policy()["policy"])

    @app.post("/v1/coach/method-policy/my-options")
    def private_options(body: MethodOptionsRequest, session=Depends(db), owner=Depends(principal)):
        return recommendations(
            body.dish_title, body.ingredients, effective_policy(session, owner.user_id)["policy"]
        )

    @app.put("/v1/coach/method-policy")
    def save(body: RuleUpdate, session=Depends(db), owner=Depends(reviewer)):
        if not body.reviewed:
            raise DomainError("REVIEW_REQUIRED", "Review method recommendations before activating", 422)
        parse_policy(body.yaml_text)
        previous = effective_policy(session, owner.user_id)
        if previous["revision"] != body.expected_revision:
            raise DomainError("SOURCE_CONFLICT", "Policy changed; reload before saving", 409)
        session.add(
            CulinarySourceRevision(
                owner_id=owner.user_id,
                source_key="method_policy",
                number=body.expected_revision + 1,
                yaml_text=body.yaml_text,
            )
        )
        audit(session, owner.user_id, "method_policy_reviewed", revision=body.expected_revision + 1)
        session.commit()
        return effective_policy(session, owner.user_id)
