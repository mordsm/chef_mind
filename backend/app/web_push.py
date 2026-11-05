"""Durable Web Push delivery for elapsed timers, independent of open browser tabs."""

import base64
import hashlib
import json
import time
from datetime import UTC, datetime, timedelta
from urllib.parse import urlsplit

from fastapi import Depends
from pydantic import Field, field_validator
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.db import ActionLogEntry, WebPushDelivery, WebPushSubscription
from app.knowledge import DomainError
from app.schemas import StrictModel


def decode(value):
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


class PushKeys(StrictModel):
    p256dh: str = Field(min_length=80, max_length=100)
    auth: str = Field(min_length=20, max_length=30)

    @field_validator("p256dh")
    @classmethod
    def public_point(cls, value):
        from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1, EllipticCurvePublicKey

        EllipticCurvePublicKey.from_encoded_point(SECP256R1(), decode(value))
        return value

    @field_validator("auth")
    @classmethod
    def secret_length(cls, value):
        if len(decode(value)) != 16:
            raise ValueError("Push auth key must be 16 bytes")
        return value


class SubscriptionInput(StrictModel):
    endpoint: str = Field(max_length=2000)
    keys: PushKeys
    expirationTime: int | None = None

    @field_validator("endpoint")
    @classmethod
    def browser_push_service(cls, value):
        parsed = urlsplit(value)
        host = (parsed.hostname or "").lower()
        # Browser-generated subscriptions only; never make arbitrary server-side HTTP requests.
        allowed = host in {
            "fcm.googleapis.com",
            "updates.push.services.mozilla.com",
            "push.services.mozilla.com",
        } or host.endswith((".notify.windows.com", ".push.apple.com"))
        if (
            parsed.scheme != "https"
            or not allowed
            or parsed.username
            or parsed.password
            or parsed.port not in (None, 443)
            or parsed.fragment
        ):
            raise ValueError("Unsupported browser push provider")
        return value


def validate_push_settings(settings):
    if not settings.push_enabled:
        return
    from cryptography.hazmat.primitives import serialization

    if not settings.push_vapid_private_key_file or not settings.push_vapid_subject.startswith("mailto:"):
        raise ValueError("Configure a private VAPID key file and mailto subject before enabling push")
    key = serialization.load_pem_private_key(settings.push_vapid_private_key_file.read_bytes(), password=None)
    public = key.public_key().public_bytes(
        serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint
    )
    if decode(settings.push_vapid_public_key) != public:
        raise ValueError("VAPID public and private keys do not match")


def provider_send(settings, subscription, payload):
    import http_ece
    import httpx
    from cryptography.hazmat.primitives.asymmetric import ec
    from py_vapid import Vapid

    # Delegate RFC 8291 encryption and VAPID signing to the protocol libraries.
    body = http_ece.encrypt(
        json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        private_key=ec.generate_private_key(ec.SECP256R1()),
        dh=decode(subscription["keys"]["p256dh"]),
        auth_secret=decode(subscription["keys"]["auth"]),
        version="aes128gcm",
    )
    endpoint = urlsplit(subscription["endpoint"])
    signer = Vapid.from_pem(settings.push_vapid_private_key_file.read_bytes())
    headers = signer.sign(
        {
            "sub": settings.push_vapid_subject,
            "aud": f"{endpoint.scheme}://{endpoint.netloc}",
            "exp": int(time.time()) + 12 * 3600,
        }
    )
    headers.update(
        {
            "TTL": "3600",
            "Urgency": "high",
            "Content-Encoding": "aes128gcm",
            "Content-Type": "application/octet-stream",
        }
    )
    response = httpx.post(
        subscription["endpoint"], content=body, headers=headers, timeout=8, follow_redirects=False
    )
    response.raise_for_status()


def dispatch_once(sessions, settings, sender=None, clock=None):
    """Leased retries survive restarts; notification tags collapse duplicate delivery."""
    from httpx import HTTPError

    clock = clock or datetime.now(UTC)
    sender = sender or (lambda subscription, payload: provider_send(settings, subscription, payload))
    with sessions() as db:
        due = db.scalars(
            select(ActionLogEntry)
            .where(
                ActionLogEntry.deleted == 0,
                ActionLogEntry.alert_at <= clock,
                ActionLogEntry.alert_at >= clock - timedelta(hours=1),
            )
            .order_by(ActionLogEntry.alert_at.desc())
            .limit(1000)
        ).all()
        for entry in due:
            subscriptions = db.scalars(
                select(WebPushSubscription).where(
                    WebPushSubscription.owner_id == entry.owner_id, WebPushSubscription.active == 1
                )
            ).all()
            for subscription in subscriptions:
                target = entry.alert_at.replace(tzinfo=UTC)
                if subscription.created_at.replace(tzinfo=UTC) > target:
                    continue
                delivery_id = hashlib.sha256(
                    (entry.id + subscription.id + target.isoformat()).encode()
                ).hexdigest()
                if not db.get(WebPushDelivery, (entry.owner_id, delivery_id)):
                    try:
                        with db.begin_nested():
                            db.add(
                                WebPushDelivery(
                                    owner_id=entry.owner_id,
                                    id=delivery_id,
                                    report_id=entry.id,
                                    subscription_id=subscription.id,
                                    target_at=target,
                                    status="pending",
                                    attempts=0,
                                    next_attempt_at=clock,
                                    lease_until=clock,
                                )
                            )
                            db.flush()
                    except IntegrityError:
                        pass
        db.commit()
        jobs = [
            (row.owner_id, row.id)
            for row in db.scalars(
                select(WebPushDelivery)
                .where(
                    WebPushDelivery.status == "pending",
                    WebPushDelivery.next_attempt_at <= clock,
                    WebPushDelivery.lease_until <= clock,
                )
                .limit(50)
            ).all()
        ]
    sent = 0
    for owner_id, job_id in jobs:
        with sessions() as db:
            claimed = db.execute(
                update(WebPushDelivery)
                .where(
                    WebPushDelivery.owner_id == owner_id,
                    WebPushDelivery.id == job_id,
                    WebPushDelivery.status == "pending",
                    WebPushDelivery.lease_until <= clock,
                    WebPushDelivery.next_attempt_at <= clock,
                )
                .values(lease_until=clock + timedelta(seconds=120))
            )
            if claimed.rowcount != 1:
                db.rollback()
                continue
            db.commit()
            job = db.get(WebPushDelivery, (owner_id, job_id))
            entry = db.get(ActionLogEntry, (owner_id, job.report_id))
            subscription = db.get(WebPushSubscription, (owner_id, job.subscription_id))
            valid = (
                entry
                and not entry.deleted
                and entry.alert_at
                and entry.alert_at.replace(tzinfo=UTC) == job.target_at.replace(tzinfo=UTC)
                and subscription
                and subscription.active
                and clock - job.target_at.replace(tzinfo=UTC) <= timedelta(hours=1)
            )
            if not valid:
                job.status = "cancelled"
                db.commit()
                continue
            # Do not include notes, ingredient details or account IDs on the lock screen.
            payload = {
                "title": "הגיע זמן לבדוק את הבישול",
                "body": "הזמן שתכננת הסתיים. פתח את המטבח ובדוק את המנה.",
                "tag": job.id,
                "url": "/report/",
                "cooking_id": entry.cooking_id,
            }
            subscription_info = subscription.document
        try:
            sender(subscription_info, payload)
            outcome = "sent"
            status_code = None
        except (OSError, ValueError, HTTPError) as error:
            response = getattr(error, "response", None)
            status_code = getattr(response, "status_code", None)
            outcome = "expired" if status_code in (404, 410) else "retry"
        with sessions() as db:
            job = db.get(WebPushDelivery, (owner_id, job_id))
            job.attempts += 1
            if outcome == "sent":
                job.status = "sent"
                sent += 1
            elif outcome == "expired":
                job.status = "expired"
                subscription = db.get(WebPushSubscription, (owner_id, job.subscription_id))
                if subscription:
                    subscription.active = 0
            elif job.attempts >= 6:
                job.status = "failed"
            else:
                job.next_attempt_at = clock + timedelta(seconds=min(900, 15 * 2**job.attempts))
                job.lease_until = clock
            db.commit()
    return {"sent": sent}


def install_push_routes(app, db_dependency, principal, sessions, settings):
    @app.get("/v1/action-log/push/status")
    def push_status():
        return {
            "enabled": settings.push_enabled,
            "public_key": settings.push_vapid_public_key if settings.push_enabled else "",
        }

    @app.post("/v1/action-log/push/subscriptions")
    def register(body: SubscriptionInput, owner=Depends(principal), db=Depends(db_dependency)):
        if not settings.push_enabled:
            raise DomainError("PUSH_DISABLED", "Enable and configure server Web Push first", 409)
        subscription_id = hashlib.sha256(body.endpoint.encode()).hexdigest()
        db.execute(
            update(WebPushSubscription)
            .where(WebPushSubscription.id == subscription_id, WebPushSubscription.owner_id != owner.user_id)
            .values(active=0)
        )
        row = db.get(WebPushSubscription, (owner.user_id, subscription_id))
        if not row:
            row = WebPushSubscription(
                owner_id=owner.user_id, id=subscription_id, document=body.model_dump(), active=1
            )
            db.add(row)
        else:
            row.document = body.model_dump()
            row.active = 1
        db.commit()
        return {"registered": True}

    @app.post("/v1/action-log/push/unsubscribe")
    def unsubscribe(body: SubscriptionInput, owner=Depends(principal), db=Depends(db_dependency)):
        key = hashlib.sha256(body.endpoint.encode()).hexdigest()
        db.execute(
            update(WebPushSubscription)
            .where(WebPushSubscription.owner_id == owner.user_id, WebPushSubscription.id == key)
            .values(active=0)
        )
        db.commit()
        return {"unsubscribed": True}

    @app.post("/v1/action-log/push/dispatch")
    def dispatch(owner=Depends(principal)):
        if owner.role != "reviewer":
            raise DomainError("FORBIDDEN", "Scheduler access requires the reviewer role", 403)
        if not settings.push_enabled:
            raise DomainError("PUSH_DISABLED", "Server push is disabled", 409)
        return dispatch_once(sessions, settings)
