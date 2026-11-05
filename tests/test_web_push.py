import base64
from datetime import UTC, datetime, timedelta
from threading import Event
from uuid import uuid4

import pytest
from app.db import WebPushDelivery, WebPushSubscription, session_factory
from app.web_push import dispatch_once
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from sqlalchemy import select
from test_action_log import mutation, report, setup_session


def subscription():
    public = (
        ec.generate_private_key(ec.SECP256R1())
        .public_key()
        .public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    )
    return {
        "endpoint": "https://fcm.googleapis.com/fcm/send/test-device",
        "expirationTime": None,
        "keys": {
            "p256dh": base64.urlsafe_b64encode(public).decode().rstrip("="),
            "auth": base64.urlsafe_b64encode(b"1234567890123456").decode().rstrip("="),
        },
    }


def test_transport_encrypts_for_receiver_and_signs_without_network(tmp_path, monkeypatch):
    import json
    from types import SimpleNamespace

    import http_ece
    import httpx
    from app.web_push import provider_send

    receiver = ec.generate_private_key(ec.SECP256R1())
    vapid = ec.generate_private_key(ec.SECP256R1())
    path = tmp_path / "vapid.pem"
    path.write_bytes(
        vapid.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
        )
    )
    public = receiver.public_key().public_bytes(
        serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint
    )
    value = subscription()
    value["keys"]["p256dh"] = base64.urlsafe_b64encode(public).decode().rstrip("=")
    secret = b"1234567890123456"
    payload = {"title": "Timer elapsed", "tag": "test-job"}
    calls = []

    def post(url, **kwargs):
        assert kwargs["headers"]["Authorization"].startswith("vapid ")
        assert kwargs["headers"]["Content-Encoding"] == "aes128gcm"
        assert not kwargs["follow_redirects"]
        decoded = http_ece.decrypt(
            kwargs["content"], private_key=receiver, auth_secret=secret, version="aes128gcm"
        )
        assert json.loads(decoded) == payload
        calls.append(url)
        return httpx.Response(201, request=httpx.Request("POST", url))

    monkeypatch.setattr("httpx.post", post)
    provider_send(
        SimpleNamespace(push_vapid_private_key_file=path, push_vapid_subject="mailto:test@example.com"),
        value,
        payload,
    )
    assert len(calls) == 1


def prepare(env):
    env["app"].state.settings.push_enabled = True
    value = subscription()
    response = env["client"].post("/v1/action-log/push/subscriptions", headers=env["headers"], json=value)
    assert response.status_code == 200
    factory = session_factory(env["engine"])
    with factory() as db:
        db.scalar(select(WebPushSubscription)).created_at = datetime.now(UTC) - timedelta(hours=2)
        db.commit()
    cooking_id, report_id = setup_session(env), str(uuid4())
    _, response = mutation(
        env["client"], env["headers"], cooking_id, "put", report_id=report_id, report=report("cook", 31)
    )
    assert response.status_code == 200
    return factory, cooking_id, report_id


def test_elapsed_timer_push_works_without_a_webpage_and_does_not_repeat(env):
    factory, _, _ = prepare(env)
    calls = []
    settings = env["app"].state.settings
    assert dispatch_once(factory, settings, lambda sub, payload: calls.append(payload))["sent"] == 1
    assert dispatch_once(factory, settings, lambda sub, payload: calls.append(payload))["sent"] == 0
    assert len(calls) == 1 and "notes" not in calls[0]


def test_transient_failure_retries_from_persistent_state(env):
    factory, _, _ = prepare(env)
    clock = datetime.now(UTC)

    def fail(*args):
        raise OSError("Simulated transport failure")

    dispatch_once(factory, env["app"].state.settings, fail, clock)
    with factory() as db:
        job = db.scalar(select(WebPushDelivery))
        assert job.status == "pending" and job.attempts == 1
    calls = []
    dispatch_once(
        factory, env["app"].state.settings, lambda *args: calls.append(args), clock + timedelta(seconds=31)
    )
    assert len(calls) == 1


def test_rescheduled_timer_cancels_an_undelivered_notification(env):
    factory, cooking_id, report_id = prepare(env)
    clock = datetime.now(UTC)

    def fail(*args):
        raise OSError("Simulated transport failure")

    dispatch_once(factory, env["app"].state.settings, fail, clock)
    value = report("cook", 31)
    value["parameters"]["duration"] = 60
    mutation(
        env["client"],
        env["headers"],
        cooking_id,
        "put",
        report_id=report_id,
        expected_revision=1,
        report=value,
    )
    calls = []
    dispatch_once(
        factory, env["app"].state.settings, lambda *args: calls.append(args), clock + timedelta(seconds=31)
    )
    assert not calls
    with factory() as db:
        assert db.scalar(select(WebPushDelivery)).status == "cancelled"


def test_expired_provider_subscription_is_deactivated(env):
    factory, _, _ = prepare(env)

    class Expired(OSError):
        response = type("Response", (), {"status_code": 410})()

    def fail(*args):
        raise Expired()

    dispatch_once(factory, env["app"].state.settings, fail)
    with factory() as db:
        assert db.scalar(select(WebPushSubscription)).active == 0
        assert db.scalar(select(WebPushDelivery)).status == "expired"


def test_subscription_moves_between_accounts_without_leaking_notifications(env):
    prepare(env)
    response = env["client"].post(
        "/v1/action-log/push/subscriptions", headers=env["other"], json=subscription()
    )
    assert response.status_code == 200
    with session_factory(env["engine"])() as db:
        assert {row.owner_id: row.active for row in db.scalars(select(WebPushSubscription))} == {
            "owner": 0,
            "other": 1,
        }


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://localhost/secret",
        "https://127.0.0.1/",
        "http://fcm.googleapis.com/path",
        "https://example.com/push",
    ],
)
def test_push_registration_cannot_request_arbitrary_server_urls(env, endpoint):
    value = subscription()
    value["endpoint"] = endpoint
    assert (
        env["client"]
        .post("/v1/action-log/push/subscriptions", headers=env["headers"], json=value)
        .status_code
        == 422
    )


def test_background_scheduler_runs_without_a_webpage(env, tmp_path, monkeypatch):
    from app.config import Settings
    from app.main import create_app
    from fastapi.testclient import TestClient

    factory, _, _ = prepare(env)
    private = ec.generate_private_key(ec.SECP256R1())
    key_path = tmp_path / "private.pem"
    key_path.write_bytes(
        private.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
        )
    )
    public = (
        base64.urlsafe_b64encode(
            private.public_key().public_bytes(
                serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint
            )
        )
        .decode()
        .rstrip("=")
    )
    settings = Settings(
        _env_file=None,
        database_url="sqlite+pysqlite:///:memory:",
        push_enabled=True,
        push_vapid_private_key_file=key_path,
        push_vapid_public_key=public,
        push_vapid_subject="mailto:test@example.com",
    )
    sent = Event()
    monkeypatch.setattr("app.web_push.provider_send", lambda *args: sent.set())
    with TestClient(create_app(settings, env["engine"])):
        assert sent.wait(5)
    with factory() as db:
        assert db.scalar(select(WebPushDelivery)).status == "sent"
