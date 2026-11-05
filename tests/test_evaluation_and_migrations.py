import os

import pytest
from alembic import command
from alembic.config import Config
from app.db import make_engine
from app.evaluation import policy_cases
from app.policies import assess
from sqlalchemy import text


@pytest.mark.parametrize(
    "name,case_request,action,expected", policy_cases(), ids=[row[0] for row in policy_cases()]
)
def test_policy_regression(name, case_request, action, expected):
    actual = assess(case_request, action)
    assert (actual[1] if actual else None) == expected


def test_evaluation_endpoint_and_schema(env):
    result = env["client"].post("/v1/evaluations/run", headers=env["headers"])
    assert result.status_code == 200 and result.json()["passed"] is True
    assert len(result.json()["cases"]) == 15
    schema = env["client"].get("/openapi.json").json()
    assert "/v1/chef/respond" in schema["paths"]
    assert "HTTPBearer" in schema["components"]["securitySchemes"]
    assert env["client"].get("/ready").status_code == 200


def test_migration_round_trip_sqlite(tmp_path, monkeypatch):
    from app.config import get_settings

    url = f"sqlite+pysqlite:///{tmp_path / 'migration.sqlite'}"
    monkeypatch.setenv("CHEF_DATABASE_URL", url)
    get_settings.cache_clear()
    try:
        command.upgrade(Config("alembic.ini"), "head")
        with make_engine(url).connect() as conn:
            assert conn.execute(text("SELECT version_num FROM alembic_version")).scalar() == "0003"
            assert conn.execute(text("SELECT COUNT(*) FROM culinary_source_revisions")).scalar() == 0
        command.downgrade(Config("alembic.ini"), "base")
        command.upgrade(Config("alembic.ini"), "head")
    finally:
        get_settings.cache_clear()


@pytest.mark.postgres
def test_postgres_real_vector_workflow(tmp_path, monkeypatch, document):
    url = os.environ.get("CHEF_TEST_POSTGRES_URL")
    if not url:
        pytest.skip("Dedicated PostgreSQL test database not configured")
    from sqlalchemy.engine import make_url

    if not (make_url(url).database or "").endswith("_test"):
        pytest.fail("Refusing to migrate/reset a database without a _test suffix")
    from app.config import Settings, get_settings
    from app.main import create_app
    from conftest import OWNER, approve, chef_body, import_doc
    from fastapi.testclient import TestClient

    monkeypatch.setenv("CHEF_DATABASE_URL", url)
    get_settings.cache_clear()
    try:
        config = Config("alembic.ini")
        command.upgrade(config, "head")
        command.downgrade(config, "base")
        command.upgrade(config, "head")
        root = tmp_path / "vault"
        (root / "owner").mkdir(parents=True)
        settings = Settings(
            database_url=url, vault_root=root, api_keys={OWNER: {"user_id": "owner", "role": "reviewer"}}
        )
        engine = make_engine(url)
        with TestClient(create_app(settings, engine)) as client:
            env = {"client": client, "root": root, "headers": {"Authorization": f"Bearer {OWNER}"}}
            draft = import_doc(env, document)
            assert approve(env, draft).status_code == 200
            result = client.post("/v1/chef/respond", headers=env["headers"], json=chef_body())
            assert result.status_code == 200, result.text
            assert result.json()["citations"][0]["revision_id"] == draft["id"]
            assert client.get("/ready").json()["storage"] == "postgresql"
        engine.dispose()
    finally:
        get_settings.cache_clear()
