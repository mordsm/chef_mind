"""Owner-scoped offline report synchronization; no language model interpretation."""

import asyncio
import hashlib
import json
import math
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal
from uuid import UUID

from fastapi import Depends, Query, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import AwareDatetime, Field, StrictFloat, StrictInt, StrictStr, model_validator
from sqlalchemy import func, select, update

from app.db import ActionLogEntry, ActionLogMutation, ActionLogSession, CookingRecord
from app.knowledge import DomainError
from app.schemas import StrictModel

ROOT = Path(__file__).with_name("static") / "report"


def configuration():
    data = json.loads((ROOT / "actions.json").read_text(encoding="utf-8"))
    ids = [action["id"] for action in data["actions"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate action ID")
    for action in data["actions"]:
        fields = action["fields"]
        if len({field["id"] for field in fields}) != len(fields):
            raise ValueError("Duplicate action field")
        if any(field["type"] not in ("number", "choice", "ingredient") for field in fields):
            raise ValueError("Unsupported action field type")
        if action["auto_timer"] and not any(
            field["id"] == "duration" and field["type"] == "number" for field in fields
        ):
            raise ValueError("Timer actions require a numeric duration in minutes")
    return data


class ReportInput(StrictModel):
    action_type: str = Field(min_length=1, max_length=80)
    config_version: int = Field(ge=1)
    parameters: dict[str, StrictStr | StrictInt | StrictFloat | None] = Field(max_length=30)
    started_at: AwareDatetime
    ended_at: AwareDatetime | None = None
    notes: str = Field(default="", max_length=2000)
    recipe_snapshot_id: str = Field(default='',max_length=80)
    recipe_step_id: str = Field(default='',max_length=80)

    @model_validator(mode="after")
    def end_order(self):
        if self.ended_at is not None and self.ended_at < self.started_at:
            raise ValueError("End precedes start")
        return self


class Mutation(StrictModel):
    request_id: UUID
    kind: Literal["create_session", "put", "delete"]
    cooking_id: UUID
    report_id: UUID | None = None
    expected_revision: int = Field(default=0, ge=0)
    report: ReportInput | None = None
    recipe_id: str = Field(default="", max_length=80)
    linked_cooking_id: str = Field(default="", max_length=80)

    @model_validator(mode="after")
    def shape(self):
        if self.kind == "create_session":
            if self.report_id or self.report or self.expected_revision:
                raise ValueError("Session creation has no report/revision")
        elif not self.report_id or (self.kind == "put") != (self.report is not None):
            raise ValueError("Invalid report mutation")
        elif self.recipe_id or self.linked_cooking_id:
            raise ValueError("Session metadata belongs to session creation")
        return self


def validated_document(report):
    config = configuration()
    action = next((item for item in config["actions"] if item["id"] == report.action_type), None)
    if not action or report.config_version != config["version"]:
        raise DomainError("CONFIG_CHANGED", "Refresh the action definitions before submitting", 422)
    if set(report.parameters) != {field["id"] for field in action["fields"]}:
        raise DomainError("INVALID_PARAMETERS", "Parameters must match the action definition", 422)
    if report.action_type == 'measure' and report.parameters.get('temperature') is None:
        raise DomainError('INVALID_PARAMETERS', 'An actual food temperature measurement is required', 422)
    ingredients = {item["id"] for item in config["ingredients"]}
    for field in action["fields"]:
        value = report.parameters[field["id"]]
        if field["type"] == "number":
            if value is None and field.get("nullable"):
                continue
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise DomainError("INVALID_PARAMETERS", "A finite numeric value is required", 422)
            if not field["min"] <= value <= field["max"]:
                raise DomainError("INVALID_PARAMETERS", "Number is outside configured bounds", 422)
        else:
            allowed = (
                ingredients if field["type"] == "ingredient" else {item["id"] for item in field["options"]}
            )
            if not isinstance(value, str) or value not in allowed:
                raise DomainError("INVALID_PARAMETERS", "Choose a configured option", 422)
    document = report.model_dump(mode="json")
    document["scheduled_end_at"] = (
        (report.started_at + timedelta(minutes=report.parameters["duration"])).isoformat()
        if action["auto_timer"]
        else None
    )
    return document


def session_payload(row):
    return {
        "id": row.id,
        "recipe_id": row.recipe_id,
        "linked_cooking_id": row.linked_cooking_id,
        "revision": row.revision,
        "created_at": row.created_at.replace(tzinfo=UTC).isoformat(),
    }


def entry_payload(row):
    result = {
        **row.document,
        "id": row.id,
        "cooking_id": row.cooking_id,
        "revision": row.revision,
        "deleted": bool(row.deleted),
        "received_at": row.received_at.replace(tzinfo=UTC).isoformat(),
    }
    deadline = result.get("scheduled_end_at")
    result["timer_elapsed_at"] = (
        deadline
        if deadline
        and datetime.fromisoformat(deadline) <= datetime.now(UTC)
        and not result.get("ended_at")
        and not row.deleted
        else None
    )
    return result


def apply_mutation(db, owner_id, body):
    raw = body.model_dump(mode="json")
    digest = hashlib.sha256(
        json.dumps(raw, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()
    ).hexdigest()
    receipt = db.get(ActionLogMutation, (owner_id, str(body.request_id)))
    if receipt:
        if receipt.body_hash != digest:
            raise DomainError("RETRY_MISMATCH", "Retry IDs cannot be reused with different content", 409)
        return receipt.result
    cooking_id = str(body.cooking_id)
    row = db.get(ActionLogSession, (owner_id, cooking_id))
    if body.kind == "create_session":
        if row:
            raise DomainError("SESSION_EXISTS", "Session ID is already in use", 409)
        if body.linked_cooking_id and not db.scalar(
            select(CookingRecord.id).where(
                CookingRecord.owner_id == owner_id, CookingRecord.cooking_id == body.linked_cooking_id
            )
        ):
            raise DomainError("NOT_FOUND", "Linked cooking session not found", 404)
        row = ActionLogSession(
            owner_id=owner_id,
            id=cooking_id,
            recipe_id=body.recipe_id,
            linked_cooking_id=body.linked_cooking_id,
            revision=0,
        )
        db.add(row)
        db.flush()
        result = {"session": session_payload(row)}
    else:
        if not row:
            raise DomainError("NOT_FOUND", "Cooking report session not found", 404)
        report_id = str(body.report_id)
        entry = db.get(ActionLogEntry, (owner_id, report_id))
        if entry and entry.cooking_id != cooking_id:
            raise DomainError("NOT_FOUND", "Report not found in this cooking session", 404)
        if (entry.revision if entry else 0) != body.expected_revision or (entry and entry.deleted):
            return JSONResponse(
                status_code=409,
                content={"code": "REPORT_CONFLICT", "current": entry_payload(entry) if entry else None},
            )
        if body.kind == "delete" and not entry:
            raise DomainError("NOT_FOUND", "Report not found", 404)
        document = validated_document(body.report) if body.report else entry.document
        alert_at = (
            datetime.fromisoformat(document["scheduled_end_at"])
            if document.get("scheduled_end_at") and not document.get("ended_at") and body.kind != "delete"
            else None
        )
        if entry is None:
            count = db.scalar(
                select(func.count())
                .select_from(ActionLogEntry)
                .where(ActionLogEntry.owner_id == owner_id, ActionLogEntry.cooking_id == cooking_id)
            )
            if count >= 1000:
                raise DomainError("SESSION_LIMIT", "Start another cooking session after 1000 reports", 422)
            entry = ActionLogEntry(
                owner_id=owner_id,
                id=report_id,
                cooking_id=cooking_id,
                revision=1,
                document=document,
                deleted=0,
                alert_at=alert_at,
            )
            db.add(entry)
            db.flush()
        else:
            changed = db.execute(
                update(ActionLogEntry)
                .where(
                    ActionLogEntry.owner_id == owner_id,
                    ActionLogEntry.id == report_id,
                    ActionLogEntry.revision == body.expected_revision,
                    ActionLogEntry.deleted == 0,
                )
                .values(
                    document=document,
                    revision=body.expected_revision + 1,
                    deleted=int(body.kind == "delete"),
                    received_at=datetime.now(UTC),
                    alert_at=alert_at,
                )
            )
            if changed.rowcount != 1:
                db.rollback()
                entry = db.get(ActionLogEntry, (owner_id, report_id))
                return JSONResponse(
                    status_code=409,
                    content={"code": "REPORT_CONFLICT", "current": entry_payload(entry) if entry else None},
                )
            db.refresh(entry)
        db.execute(
            update(ActionLogSession)
            .where(ActionLogSession.owner_id == owner_id, ActionLogSession.id == cooking_id)
            .values(revision=ActionLogSession.revision + 1)
        )
        db.refresh(row)
        result = {"report": entry_payload(entry), "session": session_payload(row)}
    db.add(
        ActionLogMutation(owner_id=owner_id, request_id=str(body.request_id), body_hash=digest, result=result)
    )
    db.commit()
    return result


def install_action_log(app, db_dependency, principal, sessions):
    configuration()  # Fail startup on an unsupported configuration.

    @app.get("/report/", include_in_schema=False)
    def report_page():
        return FileResponse(ROOT / "index.html")

    @app.get("/report/sw.js", include_in_schema=False)
    def service_worker():
        return FileResponse(ROOT / "sw.js", media_type="application/javascript")

    @app.get("/v1/action-log/config")
    def public_config():
        return configuration()

    @app.get("/v1/action-log/sessions")
    def list_sessions(owner=Depends(principal), db=Depends(db_dependency)):
        rows = db.scalars(
            select(ActionLogSession)
            .where(ActionLogSession.owner_id == owner.user_id)
            .order_by(ActionLogSession.created_at.desc())
            .limit(100)
        ).all()
        return {"items": [session_payload(row) for row in rows], "server_time": datetime.now(UTC).isoformat()}

    @app.get("/v1/action-log/sessions/{cooking_id}")
    async def snapshot(
        cooking_id: UUID,
        request: Request,
        after: int = Query(default=-1, ge=-1),
        wait: int = Query(default=0, ge=0, le=20),
        owner=Depends(principal),
    ):
        deadline = asyncio.get_running_loop().time() + wait
        while True:
            # Never keep a DB connection/transaction while waiting for another device.
            with sessions() as db:
                row = db.get(ActionLogSession, (owner.user_id, str(cooking_id)))
                if not row:
                    raise DomainError("NOT_FOUND", "Cooking report session not found", 404)
                if row.revision != after:
                    rows = db.scalars(
                        select(ActionLogEntry)
                        .where(ActionLogEntry.owner_id == owner.user_id, ActionLogEntry.cooking_id == row.id)
                        .order_by(ActionLogEntry.received_at, ActionLogEntry.id)
                    ).all()
                    return {
                        "session": session_payload(row),
                        "reports": [entry_payload(entry) for entry in rows],
                    }
            if asyncio.get_running_loop().time() >= deadline or await request.is_disconnected():
                return {"unchanged": True, "revision": after}
            await asyncio.sleep(0.4)

    @app.post("/v1/action-log/mutations")
    def mutate(body: Mutation, owner=Depends(principal), db=Depends(db_dependency)):
        return apply_mutation(db, owner.user_id, body)
