import copy

import pytest
import yaml
from app.config import Settings
from app.db import Base, make_engine
from app.main import create_app
from fastapi.testclient import TestClient

OWNER = "owner-test-token-at-least-24-characters"
OTHER = "other-test-token-at-least-24-characters"
COOK = "cook-test-token-at-least-24-characters"


@pytest.fixture
def env(tmp_path):
    root = tmp_path / "vault"
    for owner in ("owner", "other"):
        (root / owner).mkdir(parents=True)
    settings = Settings(
        database_url="sqlite+pysqlite:///:memory:",
        vault_root=root,
        api_keys={
            OWNER: {"user_id": "owner", "role": "reviewer"},
            OTHER: {"user_id": "other", "role": "reviewer"},
            COOK: {"user_id": "owner", "role": "cook"},
        },
    )
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)
    app = create_app(settings, engine)
    with TestClient(app) as client:
        yield {
            "client": client,
            "app": app,
            "root": root,
            "engine": engine,
            "headers": {"Authorization": f"Bearer {OWNER}"},
            "other": {"Authorization": f"Bearer {OTHER}"},
            "cook": {"Authorization": f"Bearer {COOK}"},
        }
    engine.dispose()


@pytest.fixture
def document():
    return {
        "source_id": "onion-source",
        "title": "Original onion note",
        "source_reference": "Original test author",
        "license_status": "original",
        "license_reference": "Test fixture written for this project",
        "units": [
            {
                "knowledge_id": "onion-heat",
                "title": "onion browning",
                "principle": "Lower heat slows browning.",
                "conditions": [],
                "observations": ["Report whether browning slows."],
                "recommended_action": "Lower the heat and monitor the onion.",
                "tags": ["onion", "browning", "בצל"],
                "confidence": 70,
                "verified_on": "2026-10-19",
            }
        ],
    }


def write_document(env, document, path="note.md", owner="owner"):
    target = env["root"] / owner / path
    target.write_text(
        "---\n" + yaml.safe_dump(copy.deepcopy(document), allow_unicode=True) + "---\nOriginal body.\n",
        encoding="utf-8",
    )
    return target


def import_doc(env, document, key="import-test-001"):
    write_document(env, document)
    result = env["client"].post(
        "/v1/knowledge/import", headers=env["headers"], json={"path": "note.md", "idempotency_key": key}
    )
    assert result.status_code == 201, result.text
    return result.json()


def approve(env, draft):
    return env["client"].post(
        f"/v1/knowledge/{draft['id']}/approve",
        headers=env["headers"],
        json={"expected_revision": draft["revision"], "reason": "Human reviewed fixture and authorization"},
    )


def chef_body(cooking_id="dinner"):
    return {"cooking_id": cooking_id, "message": "onion browning", "state": {"current_goal": "soft onion"}}
