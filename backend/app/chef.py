"""Extractive grounded baseline. No model claims, inferred observations or sensor access."""

from app.knowledge import active_rows
from app.policies import assess, missing_ingredients
from app.retrieval import retrieve
from app.schemas import ChefDecision, Citation


def non_action(request, kind, flag, message):
    return ChefDecision(
        decision_type=kind,
        current_goal=request.state.current_goal,
        instruction=message,
        culinary_reason="נדרש מידע או אישור לפני הצעת פעולה מבוססת.",
        success_signal="המידע החסר אומת לפני המשך הפעולה.",
        response_text=message,
        rationale="לא הוסקו מדידות, מלאי או עובדות שלא דווחו.",
        confidence=0,
        policy_flags=[flag],
        safety_flags=[flag] if "SAFETY" in flag or "ALLERGEN" in flag else [],
    )


def respond(session, owner, request, selection=None):
    policy = assess(request)
    if policy:
        return non_action(request, *policy)
    missing = missing_ingredients(request, request.essential_ingredients)
    if missing:
        return non_action(
            request,
            "clarify",
            "INVENTORY_UNVERIFIED",
            "האם יש לך כמות מאומתת של: " + ", ".join(missing) + "?",
        )
    query = " ".join([request.message, request.state.current_goal, *request.state.reports])
    matches = retrieve(session, owner, query)
    if not matches:
        decision = non_action(
            request,
            "insufficient_evidence",
            "NO_APPROVED_EVIDENCE",
            "אין עדיין מתכון מאושר למנה הזו; אפשר להיעזר ביסודות ההכנה שלהלן.",
        )
        decision.available_topics = list(
            dict.fromkeys(
                entry["title"]
                for index, revision, _ in session.execute(active_rows(session, owner).limit(12))
                for entry in revision.document["units"]
                if entry["knowledge_id"] == index.knowledge_id
            )
        )[:8]
        return decision
    if selection is not None:
        selected = [
            match
            for match in matches
            if match[1].knowledge_id == selection.knowledge_id and match[2].id == selection.revision_id
        ]
        if not selected:
            return non_action(
                request,
                "insufficient_evidence",
                "MODEL_SOURCE_STALE",
                "The selected source changed; retry with current approved knowledge.",
            )
        matches = selected + [match for match in matches if match not in selected]
    _, unit, revision, source = matches[0]
    confirmed = {value.lower() for value in request.confirmed_conditions + request.state.reports}
    if any(condition.lower() not in confirmed for condition in unit.conditions):
        missing_conditions = [
            condition for condition in unit.conditions if condition.lower() not in confirmed
        ]
        decision = non_action(
            request,
            "clarify",
            "CONDITION_UNCONFIRMED",
            "בדוק: " + "; ".join(missing_conditions) + ".",
        )
        decision.missing_conditions = missing_conditions
        # Identification advice must not require the identification to be complete first.
        # This narrowly scoped check never authorizes cooking or certifies doneness.
        if source.source_id == "bccampus-meat" and unit.knowledge_id == "collagen-moist-heat":
            decision.instruction = "בדוק שהנתח עשיר ברקמת חיבור."
            decision.response_text = decision.instruction
            decision.requires_confirmation = False
            decision.culinary_reason = ""
            decision.success_signal = ""
        decision.response_text = decision.instruction
        return decision
    if unit.exceptions:
        # No free-form exception is silently assumed false in the baseline.
        return non_action(
            request,
            "clarify",
            "EXCEPTION_REVIEW_REQUIRED",
            "לפני הפעולה יש לברר את החריגים שבמקור: " + "; ".join(unit.exceptions),
        )
    missing = missing_ingredients(request, unit.required_ingredients)
    if missing:
        return non_action(
            request, "clarify", "INVENTORY_UNVERIFIED", "יש לאמת זמינות וכמות של: " + ", ".join(missing)
        )
    if request.compare_techniques:
        alternate_matches = [
            (other, other_revision, other_source)
            for _, other, other_revision, other_source in matches
            if other.knowledge_id != unit.knowledge_id
            and not other.conditions
            and not other.exceptions
            and not missing_ingredients(request, other.required_ingredients)
            and assess(request, other.recommended_action) is None
        ]
        if not alternate_matches:
            return non_action(
                request,
                "insufficient_evidence",
                "SECOND_TECHNIQUE_UNSUPPORTED",
                "יש תמיכה מאושרת בשיטה אחת בלבד; אין די ידע מאושר להשוואת שתי טכניקות.",
            )
    else:
        alternate_matches = []
    policy = assess(request, unit.recommended_action)
    if policy:
        return non_action(request, *policy)
    citation = Citation(
        source_id=source.source_id,
        source_reference=revision.document["source_reference"],
        revision=revision.number,
        revision_id=revision.id,
        knowledge_id=unit.knowledge_id,
        supporting_text=unit.recommended_action,
        attribution=revision.document.get("attribution", ""),
        license_reference=revision.document["license_reference"],
    )
    citations = [citation]
    for other, other_revision, other_source in alternate_matches[:1]:
        citations.append(
            Citation(
                source_id=other_source.source_id,
                source_reference=other_revision.document["source_reference"],
                revision=other_revision.number,
                revision_id=other_revision.id,
                knowledge_id=other.knowledge_id,
                supporting_text=other.recommended_action,
                attribution=other_revision.document.get("attribution", ""),
                license_reference=other_revision.document["license_reference"],
            )
        )
    action = unit.recommended_action
    reason = unit.principle
    signal = "; ".join(unit.observations)
    text = f"לפי הדיווח שלך: {action} הסיבה: {reason} סימן לבדיקה: {signal}"
    if request.profile.explanation == "quiet":
        text = f"{action} בדוק ועדכן: {signal}"
    assumptions = [f"לא אומתה זמינות: {item.name}" for item in request.inventory if not item.verified]
    return ChefDecision(
        decision_type="action",
        current_goal=request.state.current_goal,
        instruction=action,
        culinary_reason=reason,
        success_signal=signal,
        response_text=text,
        proposed_action=action,
        rationale=reason,
        confidence=min(unit.confidence, 75),
        citations=citations,
        safety_flags=unit.safety_notes,
        inventory_assumptions=assumptions,
        alternatives=[other.recommended_action for other, _, _ in alternate_matches[:1]],
    )
