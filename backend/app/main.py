import hashlib
import logging
import os
import secrets
from contextlib import asynccontextmanager
from datetime import UTC
from pathlib import Path
from threading import Event, Thread
from uuid import uuid4

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.action_log import install_action_log
from app.chef import respond
from app.coach import install_coach_routes
from app.config import Settings, get_settings
from app.culinary_basics import basics_for
from app.culinary_engine_api import install_engine_routes
from app.culinary_evaluation import run_culinary_suite
from app.culinary_sources import install_source_routes
from app.db import AuditEvent, CookingRecord, Revision, Source, make_engine, session_factory
from app.evaluation import activation_gate, run_policy_suite
from app.history import lifecycle, revision_diff, source_history
from app.knowledge import (
    DomainError,
    audit,
    import_document,
    owned_revision,
    review_revision,
    revision_payload,
)
from app.method_policy import install_method_routes
from app.model import select_knowledge
from app.ontology_bridge import install_ontology_routes
from app.policies import assess
from app.problem_rules import install_problem_routes
from app.provider import ProviderMonitor, run_selection
from app.retrieval import embed, retrieve
from app.schemas import (
    ChefDecision,
    ChefRequest,
    ImportRequest,
    InventoryUpdate,
    LifecycleRequest,
    Profile,
    ReviewRequest,
)
from app.sync import reconcile
from app.web_push import dispatch_once, install_push_routes, validate_push_settings

bearer = HTTPBearer(auto_error=False)


def create_app(settings: Settings | None = None, engine=None):
    settings = settings or get_settings()
    engine = engine or make_engine(settings.database_url)
    sessions = session_factory(engine)
    validate_push_settings(settings)

    @asynccontextmanager
    async def lifespan(application):
        stop = Event()

        def poll():
            while not stop.wait(settings.poll_seconds):
                for user in sorted({p.user_id for p in settings.api_keys.values() if p.role == "reviewer"}):
                    if stop.is_set():
                        break
                    try:
                        with sessions() as scan_session:
                            reconcile(scan_session, settings.vault_root, user)
                    except (DomainError, SQLAlchemyError, OSError):
                        logging.getLogger(__name__).warning("Vault scan failed; existing knowledge retained")

        worker = Thread(target=poll, name="chef-vault-sync", daemon=True) if settings.sync_enabled else None
        def push_timers():
            while not stop.wait(1):
                try:
                    dispatch_once(sessions, settings)
                except Exception:
                    logging.getLogger(__name__).warning("Timer push dispatch failed; durable jobs retained")

        push_worker = Thread(target=push_timers, name="chef-timer-push", daemon=True) if settings.push_enabled and settings.push_worker_enabled else None
        if worker:
            worker.start()
        if push_worker:
            push_worker.start()
        try:
            yield
        finally:
            stop.set()
            if worker:
                worker.join(timeout=5)
            if push_worker:
                push_worker.join(timeout=5)

    app = FastAPI(
        title="Chef Core",
        version="0.1.0",
        description="Reviewed knowledge with optional bounded model selection and Vault reconciliation.",
        lifespan=lifespan,
    )
    app.state.engine = engine
    app.state.settings = settings
    app.state.activation_gate = activation_gate
    app.state.embed = embed
    app.state.model_selector = select_knowledge
    app.state.provider_monitor = ProviderMonitor(settings)
    static_root = Path(__file__).resolve().parent / "static"
    app.mount("/assets", StaticFiles(directory=static_root), name="console-assets")
    snapshot = Path(__file__).resolve().parents[2] / "docs" / "CHEF_CONSTITUTION_0_1.md"
    app.state.constitution_digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()

    @app.middleware("http")
    async def request_id(request: Request, call_next):
        request.state.request_id = str(uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        if request.url.path == "/" or request.url.path.startswith(("/assets/", "/report/")):
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' blob:; "
                "connect-src 'self'; frame-ancestors 'self'; base-uri 'none'; form-action 'self'"
            )
        response.headers["Cache-Control"] = "no-store"
        return response

    def failure(request, status, code, message):
        return JSONResponse(
            status_code=status,
            content={
                "code": code,
                "message": message,
                "request_id": getattr(request.state, "request_id", str(uuid4())),
            },
        )

    @app.exception_handler(DomainError)
    async def domain_error(request, exc):
        return failure(request, exc.status, exc.code, exc.message)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        # Do not reflect tokens, user text or private source material in validation errors.
        return failure(
            request, 422, "INVALID_REQUEST", "Request fields failed validation; consult the OpenAPI schema"
        )

    @app.exception_handler(IntegrityError)
    async def conflict_error(request, exc):
        return failure(
            request, 409, "WRITE_CONFLICT", "Concurrent update detected; reload and retry the same operation"
        )

    @app.exception_handler(SQLAlchemyError)
    async def storage_error(request, exc):
        return failure(
            request,
            503,
            "STORAGE_UNAVAILABLE",
            "Storage is not ready; run migrations and check configuration",
        )

    @app.exception_handler(Exception)
    async def unexpected_error(request, exc):
        return failure(
            request,
            500,
            "INTERNAL_ERROR",
            "The operation did not complete; active knowledge was not intentionally changed",
        )

    def db():
        with sessions() as session:
            try:
                yield session
            except Exception:
                session.rollback()
                raise

    def principal(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
        if credentials:
            for key, owner in settings.api_keys.items():
                if secrets.compare_digest(credentials.credentials, key):
                    return owner
        raise DomainError("UNAUTHENTICATED", "A valid Bearer token is required", 401)

    def reviewer(owner=Depends(principal)):
        if owner.role != "reviewer":
            raise DomainError("FORBIDDEN", "Knowledge review permission is required", 403)
        return owner

    install_source_routes(app, db, principal, reviewer)
    install_problem_routes(app, db, principal, reviewer)
    install_method_routes(app, db, principal, reviewer)
    install_engine_routes(app, reviewer)
    install_ontology_routes(app, db, principal, reviewer)

    @app.get("/health")
    def health():
        return {"status": "alive", "service": "chef-core", "version": "0.1.0"}

    @app.get("/", include_in_schema=False)
    def console():
        return FileResponse(static_root / "index.html")

    @app.get("/v1/session")
    def session_identity(owner=Depends(principal)):
        return {"user_id": owner.user_id, "role": owner.role}

    @app.get("/v1/knowledge/sources")
    def source_catalog(offset: int = 0, owner=Depends(principal), session=Depends(db)):
        if offset < 0 or offset > 100_000:
            raise DomainError("INVALID_PAGE", "Offset must be between 0 and 100000", 422)
        query = select(Source).where(Source.owner_id == owner.user_id).order_by(Source.source_id)
        if owner.role != "reviewer":
            query = query.where(Source.active_revision_id.is_not(None))
        sources = session.scalars(query.offset(offset).limit(101)).all()
        items = []
        for source in sources[:100]:
            latest = session.scalar(
                select(Revision)
                .where(Revision.source_pk == source.id)
                .order_by(Revision.number.desc())
                .limit(1)
            )
            visible = latest if owner.role == "reviewer" else session.get(Revision, source.active_revision_id)
            if visible is not None:
                items.append(
                    {
                        "source_id": source.source_id,
                        "title": visible.document["title"],
                        "status": visible.status,
                        "latest_revision_id": visible.id,
                        "active_revision_id": source.active_revision_id,
                        "source_reference": visible.document.get("source_reference", ""),
                        "attribution": visible.document.get("attribution", ""),
                        "adaptation_notes": visible.document.get("adaptation_notes", ""),
                        "source_kind": "knowledge_document",
                        "usage": "advanced_advisor_after_approval",
                        "tags": list(
                            dict.fromkeys(
                                tag for unit in visible.document["units"] for tag in unit.get("tags", [])
                            )
                        ),
                        "conditions": [
                            condition
                            for unit in visible.document["units"]
                            for condition in unit.get("conditions", [])
                        ],
                    }
                )
        return {"items": items, "offset": offset, "has_more": len(sources) > 100}

    @app.get("/ready")
    def ready(session=Depends(db)):
        session.execute(select(Source.id).limit(1))
        if engine.dialect.name == "postgresql" and not session.scalar(
            text("SELECT extversion FROM pg_extension WHERE extname='vector'")
        ):
            raise DomainError("INDEX_NOT_READY", "pgvector extension is not installed", 503)
        return {"status": "ready", "storage": engine.dialect.name, "embedding": "local-char-hash-384-v1"}

    @app.post("/v1/knowledge/import", status_code=201)
    def import_source(body: ImportRequest, owner=Depends(reviewer), session=Depends(db)):
        return revision_payload(import_document(session, settings.vault_root, owner.user_id, body))

    @app.get("/v1/knowledge/pending")
    def pending(owner=Depends(reviewer), session=Depends(db)):
        rows = session.scalars(
            select(Revision)
            .join(Source)
            .where(Source.owner_id == owner.user_id, Revision.status == "pending_review")
            .order_by(Revision.created_at)
        )
        return {"items": [revision_payload(row) for row in rows]}

    @app.post("/v1/vault/sync")
    def sync_vault(owner=Depends(reviewer), session=Depends(db)):
        return reconcile(session, settings.vault_root, owner.user_id)

    @app.get("/v1/knowledge/{revision_id}")
    def knowledge(revision_id: str, owner=Depends(reviewer), session=Depends(db)):
        revision, _ = owned_revision(session, owner.user_id, revision_id)
        return revision_payload(revision)

    @app.post("/v1/knowledge/{revision_id}/approve")
    def approve(revision_id: str, body: ReviewRequest, owner=Depends(reviewer), session=Depends(db)):
        result = review_revision(
            session, owner.user_id, revision_id, body, True, app.state.embed, app.state.activation_gate
        )
        return revision_payload(result)

    @app.post("/v1/knowledge/{revision_id}/reject")
    def reject(revision_id: str, body: ReviewRequest, owner=Depends(reviewer), session=Depends(db)):
        return revision_payload(
            review_revision(
                session, owner.user_id, revision_id, body, False, app.state.embed, app.state.activation_gate
            )
        )

    @app.get("/v1/knowledge/{revision_id}/revisions")
    def history(revision_id: str, owner=Depends(reviewer), session=Depends(db)):
        return source_history(session, owner.user_id, revision_id)

    @app.get("/v1/knowledge/{revision_id}/diff/{other_id}")
    def diff(revision_id: str, other_id: str, owner=Depends(reviewer), session=Depends(db)):
        return revision_diff(session, owner.user_id, revision_id, other_id)

    @app.post("/v1/knowledge/{revision_id}/retire")
    def retire(revision_id: str, body: LifecycleRequest, owner=Depends(reviewer), session=Depends(db)):
        return lifecycle(
            session, owner.user_id, revision_id, body, "retire", app.state.embed, app.state.activation_gate
        )

    @app.post("/v1/knowledge/{revision_id}/rollback")
    def rollback(revision_id: str, body: LifecycleRequest, owner=Depends(reviewer), session=Depends(db)):
        return lifecycle(
            session, owner.user_id, revision_id, body, "rollback", app.state.embed, app.state.activation_gate
        )

    @app.post("/v1/chef/respond", response_model=ChefDecision)
    def chef(body: ChefRequest, owner=Depends(principal), session=Depends(db)):
        # Reject stale sessions and apply persisted constraints before spending an external call.
        preflight = session.scalar(
            select(CookingRecord).where(
                CookingRecord.owner_id == owner.user_id, CookingRecord.cooking_id == body.cooking_id
            )
        )
        if body.expected_state_revision != (preflight.revision if preflight else 0):
            raise DomainError(
                "STATE_CONFLICT", "Cooking state changed; read the latest state before continuing", 409
            )
        if preflight:
            previous = preflight.state["profile"]
            if "profile" not in body.model_fields_set:
                body.profile = Profile.model_validate(previous)
            elif body.profile.model_dump() != previous and not body.confirm_profile_change:
                raise DomainError(
                    "PROFILE_CHANGE_CONFIRMATION_REQUIRED",
                    "Explicit confirmation is required to change existing dietary constraints",
                    409,
                )
        selection = None
        model_failed = False
        provider_status = "disabled" if not settings.model_enabled else "not_requested"
        provider_latency = None
        pre_policy = assess(body)
        if settings.model_enabled and body.allow_external_model and pre_policy is not None:
            provider_status = "policy_blocked"
        if settings.model_enabled and body.allow_external_model and pre_policy is None:
            provider_status = "no_candidates"
            candidates = retrieve(
                session, owner.user_id, " ".join([body.message, body.state.current_goal, *body.state.reports])
            )
            # No database transaction or row lock spans an external API call.
            session.rollback()
            if candidates:
                # Snapshot scalar data before rollback expiration can reload a transaction.
                from types import SimpleNamespace

                candidates = [
                    (score, unit, SimpleNamespace(id=revision.id), None)
                    for score, unit, revision, _ in candidates
                ]
                session.rollback()
                selection, provider_status, provider_latency = run_selection(
                    settings,
                    body,
                    candidates,
                    app.state.model_selector,
                    app.state.provider_monitor,
                    owner.user_id,
                )
                model_failed = selection is None
        record = session.scalar(
            select(CookingRecord)
            .where(CookingRecord.owner_id == owner.user_id, CookingRecord.cooking_id == body.cooking_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        current = record.revision if record else 0
        if body.expected_state_revision != current:
            raise DomainError(
                "STATE_CONFLICT", "Cooking state changed; read the latest state before continuing", 409
            )
        if record:
            previous_profile = record.state["profile"]
            if "profile" not in body.model_fields_set:
                body.profile = Profile.model_validate(previous_profile)
            elif body.profile.model_dump() != previous_profile and not body.confirm_profile_change:
                raise DomainError(
                    "PROFILE_CHANGE_CONFIRMATION_REQUIRED",
                    "Explicit confirmation is required to change existing dietary constraints",
                    409,
                )
        decision = respond(session, owner.user_id, body, selection)
        from app.culinary_context import dish_context
        from app.station_protocol import build_protocol

        station_title = body.state.current_goal or body.message
        station_context = dish_context(station_title, "", [item.name for item in body.inventory])
        decision.station_protocol = build_protocol(
            station_title, family=station_context["family"], advice=decision.instruction,
            current={"title": "הפעולה הנוכחית", "instruction": decision.instruction,
                     "successCriteria": [decision.success_signal]} if decision.decision_type == "action" else None,
            blocked=decision.decision_type == "blocked" or bool(decision.missing_conditions)
            or "INVENTORY_UNVERIFIED" in decision.policy_flags or "EXCEPTION_REVIEW_REQUIRED" in decision.policy_flags
            or "INGREDIENT_COMPOSITION_UNKNOWN" in decision.policy_flags,
            gaps=["הנחיית המקור: " + decision.instruction] if decision.decision_type != "action" else (),
            model_status="unavailable" if model_failed else "rules_only",
            allergies=body.profile.allergies,
            ingredients=[item.name for item in body.inventory],
            user_message=body.message,
        )
        if decision.citations:
            from app.station_protocol import obsidian_note, render_text

            protocol = decision.station_protocol
            protocol["action_citations"] = [citation.model_dump(mode="json") for citation in decision.citations]
            protocol["blocks"][5]["text"] += "\nמקורות מאושרים לפעולה: " + "; ".join(
                f"{citation.source_id} / {citation.knowledge_id}: {citation.source_reference}"
                for citation in decision.citations
            )
            protocol["source_ids"] = list(dict.fromkeys([
                *protocol["source_ids"], *[citation.source_id for citation in decision.citations]
            ]))
            protocol["text"] = render_text(protocol)
            protocol["obsidian_markdown"] = obsidian_note(protocol, station_title)
        if decision.decision_type != "blocked":
            decision.basic_knowledge = basics_for(body.state.current_goal + " " + body.message)
        if selection is not None:
            decision.engine_version = "openai-approved-selector-v1"
        if model_failed:
            decision.policy_flags.append("MODEL_UNAVAILABLE_EXTRACTIVE_FALLBACK")
            decision.policy_flags.append("MODEL_" + provider_status.upper())
        decision.provider_status = provider_status
        decision.provider_latency_ms = provider_latency
        decision.constitution_digest = app.state.constitution_digest
        decision.state_revision = current + 1
        original_goal = record.state.get("original_goal") if record else body.state.current_goal
        state = {
            "original_goal": original_goal,
            "reported_state": body.state.model_dump(),
            "profile": body.profile.model_dump(),
            "inventory": [item.model_dump() for item in body.inventory],
        }
        if record is None:
            record = CookingRecord(owner_id=owner.user_id, cooking_id=body.cooking_id)
            session.add(record)
        record.revision = current + 1
        record.state, record.decision = state, decision.model_dump()
        audit(
            session,
            owner.user_id,
            "CHEF_DECISION",
            cooking_id=body.cooking_id,
            state_revision=record.revision,
            decision_type=decision.decision_type,
            citation_revision_ids=[c.revision_id for c in decision.citations],
            engine=decision.engine_version,
            constitution=decision.constitution_version,
            constitution_digest=decision.constitution_digest,
            policy=decision.policy_version,
            provider_status=provider_status,
            provider_latency_ms=provider_latency,
        )
        session.commit()
        return decision

    @app.get("/v1/inventory")
    def saved_inventory(owner=Depends(principal), session=Depends(db)):
        saved = session.scalar(
            select(AuditEvent)
            .where(AuditEvent.owner_id == owner.user_id, AuditEvent.action == "INVENTORY_SAVED")
            .order_by(AuditEvent.created_at.desc())
            .limit(1)
        )
        if saved is not None:
            return {
                "items": saved.details["items"],
                "origin": "saved",
                "updated_at": saved.created_at.replace(tzinfo=UTC).isoformat(),
            }
        # Recover pre-feature inventory by decision date, never by random UUID order.
        events = session.scalars(
            select(AuditEvent)
            .where(AuditEvent.owner_id == owner.user_id, AuditEvent.action == "CHEF_DECISION")
            .order_by(AuditEvent.created_at.desc())
        )
        seen = set()
        for event in events:
            cooking_id = event.details.get("cooking_id")
            if not cooking_id or cooking_id in seen:
                continue
            seen.add(cooking_id)
            record = session.scalar(
                select(CookingRecord).where(
                    CookingRecord.owner_id == owner.user_id, CookingRecord.cooking_id == cooking_id
                )
            )
            if record and record.state.get("inventory"):
                return {"items": record.state["inventory"], "origin": "recovered"}
        return {"items": [], "origin": "empty"}

    @app.get("/v1/inventory/history")
    def inventory_history(owner=Depends(principal), session=Depends(db)):
        events = session.scalars(
            select(AuditEvent)
            .where(AuditEvent.owner_id == owner.user_id, AuditEvent.action == "CHEF_DECISION")
            .order_by(AuditEvent.created_at.desc())
            .limit(500)
        )
        seen, items = set(), []
        for event in events:
            cooking_id = event.details.get("cooking_id")
            if not cooking_id or cooking_id in seen:
                continue
            seen.add(cooking_id)
            record = session.scalar(
                select(CookingRecord).where(
                    CookingRecord.owner_id == owner.user_id, CookingRecord.cooking_id == cooking_id
                )
            )
            if record and record.state.get("inventory"):
                items.append(
                    {
                        "cooking_id": cooking_id,
                        "goal": record.state.get("reported_state", {}).get("current_goal", ""),
                        "inventory": record.state["inventory"],
                        "date": event.created_at.replace(tzinfo=UTC).isoformat(),
                    }
                )
            if len(items) >= 30:
                break
        return {"items": items}

    @app.put("/v1/inventory")
    def save_inventory(body: InventoryUpdate, owner=Depends(principal), session=Depends(db)):
        items = [item.model_dump() for item in body.items]
        event = audit(session, owner.user_id, "INVENTORY_SAVED", items=items)
        session.commit()
        return {
            "items": items,
            "origin": "saved",
            "updated_at": event.created_at.replace(tzinfo=UTC).isoformat(),
        }

    @app.get("/v1/cooking/{cooking_id}")
    def cooking(cooking_id: str, owner=Depends(principal), session=Depends(db)):
        record = session.scalar(
            select(CookingRecord).where(
                CookingRecord.owner_id == owner.user_id, CookingRecord.cooking_id == cooking_id
            )
        )
        if record is None:
            raise DomainError("NOT_FOUND", "Cooking record was not found", 404)
        return {
            "cooking_id": record.cooking_id,
            "revision": record.revision,
            "state": record.state,
            "decision": record.decision,
        }

    @app.get("/v1/operations/provider")
    def provider_operations(owner=Depends(reviewer)):
        return {
            "enabled": settings.model_enabled,
            "key_configured": bool(settings.openai_api_key or os.environ.get("OPENAI_API_KEY")),
            "model": settings.model_name,
            "timeout_seconds": settings.model_timeout_seconds,
            "max_output_tokens": settings.model_max_output_tokens,
            "per_process_calls_per_minute": settings.model_calls_per_minute,
            "per_owner_calls_per_minute": settings.model_user_calls_per_minute,
            **app.state.provider_monitor.snapshot(owner.user_id),
        }

    @app.post("/v1/evaluations/run")
    def evaluate(owner=Depends(reviewer), session=Depends(db)):
        report = run_policy_suite()
        audit(session, owner.user_id, "EVALUATION_RUN", report=report)
        session.commit()
        return report

    @app.post("/v1/evaluations/culinary")
    def culinary_evaluate(owner=Depends(reviewer), session=Depends(db)):
        report = run_culinary_suite(session, owner.user_id)
        audit(session, owner.user_id, "CULINARY_EVALUATION_RUN", report=report)
        session.commit()
        return report

    install_coach_routes(app, principal, db, settings)
    install_action_log(app, db, principal, sessions)
    install_push_routes(app, db, principal, sessions, settings)
    return app


app = create_app()
