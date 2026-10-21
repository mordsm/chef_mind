# chef_mind / Chef Core

[Open Chef](http://127.0.0.1:8800/) · [Edit culinary YAML sources and use the API](docs/CULINARY_SOURCE_CONFIGURATION.md)

The Open Chef link works while the local server is running; see Local setup below to start it.

For access from another location, run `./scripts/cloudflare.ps1 -Action Start` and open the HTTPS URL it prints. See [Cloudflare remote access](docs/REMOTE_ACCESS.md) for status, stopping, sign-in and address lifetime.

The primary interface is now a [Cooking Coach](docs/COOKING_COACH.md): a cooking journey, chef dialogue, and short contextual lessons. Start a local journey without signing in; connect for private inventory recovery and server-saved progress.

Standalone FastAPI service for approved culinary knowledge and grounded decisions. The first slice implements **Markdown → review → index activation → extractive answer with citations and policy checks**. It does not modify Cook Pilot.

This is an engineering baseline, not a professionally validated chef. Optional OpenAI selection requires server configuration and per-request opt-in. Local hash embeddings are not semantic embeddings. Do not treat time, color or response confidence as food-safety certification.

Five attributed culinary drafts, model selection, twenty cooking scenarios and automatic Vault polling are documented in [Sources and model operation](docs/SOURCES_AND_MODEL.md). New or changed knowledge always requires review before activation.

Review source history, compare revisions, retire knowledge or restore a previously approved revision using [Knowledge recovery](docs/KNOWLEDGE_RECOVERY.md).

Edit and extend the two culinary YAML source drafts through the console or authenticated API using [Culinary source configuration](docs/CULINARY_SOURCE_CONFIGURATION.md).

Choose common cooking problems and add reviewed response rules through [Problem rules](docs/PROBLEM_RULES.md). Missing rules are explicitly flagged and retained in the cooking backlog.

Restrict each dish to configurable recommended preparation methods using [Method policy](docs/METHOD_POLICY.md), including explanations for excluded methods.

Create private database/Vault archives and restore to an isolated empty target using [Backup recovery](docs/BACKUP_RECOVERY.md).

Configure model request limits and inspect owner-scoped diagnostics using [Provider operations](docs/PROVIDER_OPERATIONS.md).

Open the [local console](http://127.0.0.1:8800/) for cooking, editable inventory and knowledge review. See [Console guide](docs/LOCAL_CONSOLE.md) for the access-token distinction and privacy behavior.

Use [Kitchen view](docs/KITCHEN_VIEW.md) for large current guidance, explicit outcome reports, manual reminders and optional local browser read-aloud/screen-awake controls.

## Local setup

Python 3.12+, uv, Docker with a running engine:

```powershell
uv sync --locked
uv run python scripts/bootstrap_local.py
# The generated .env contains a private owner token; do not publish it.
docker compose --env-file .env -p chef-mind -f infra/docker-compose.yml up -d db
$env:PYTHONPATH='backend'
uv run alembic upgrade head
uv run uvicorn app.main:app --host 127.0.0.1 --port 8800
```

If uv's default cache is not writable, set `UV_CACHE_DIR` to a writable local directory such as `.uv-cache`. The environment file is ignored by Git. Keep the example database password local; replace it before any nonlocal deployment. API tokens map to stable user IDs and roles (`reviewer` or `cook`). No token is enabled by default. Tokens currently confer all permissions within the same user ID; token rotation is manual.

Open `http://127.0.0.1:8800/docs` for OpenAPI. `/health` is process liveness; `/ready` checks migrated storage and pgvector. The service does not create tables at startup; migrations are required.

## First workflow

Use a reviewer token whose configured user ID is `owner`. The original example is in `vault/owner/00_inbox/onion-demo.md`; it is not activated automatically. Set `$token` locally without committing it.

```powershell
$headers=@{Authorization="Bearer $token"}
$import=@{path='00_inbox/onion-demo.md';idempotency_key='demo-onion-import-001'} | ConvertTo-Json
$draft=Invoke-RestMethod http://127.0.0.1:8800/v1/knowledge/import -Method Post -Headers $headers -ContentType application/json -Body $import
# Read the complete draft; approve only after reviewing its contents and license.
$review=@{expected_revision=$draft.revision;reason='Reviewed original engineering example and limitations'} | ConvertTo-Json
Invoke-RestMethod "http://127.0.0.1:8800/v1/knowledge/$($draft.id)/approve" -Method Post -Headers $headers -ContentType application/json -Body $review
```

POST `/v1/chef/respond` with:

```json
{
  "cooking_id": "onion-demo",
  "expected_state_revision": 0,
  "message": "הבצל משחים לפני שהתרכך",
  "profile": {"forbid_meat_dairy": true, "allergies": []},
  "state": {"current_goal": "לרכך בצל בלי לשרוף", "reports": ["הבצל משחים לפני שהתרכך"]},
  "confirmed_conditions": ["הבצל משחים לפני שהתרכך"],
  "inventory": [{"name": "בצל", "quantity": 2, "unit": "whole", "verified": true, "food_class": "pareve"}]
}
```

The response includes one action, reason, success signal, source/revision citations and the new `state_revision`. Subsequent requests must use that revision. `GET /v1/cooking/onion-demo` returns only the authenticated user's record. Exact conditions are deliberately confirmed explicitly in this baseline; there is no language-model inference of observation.

Omitting `profile` on a later request preserves the stored profile. To intentionally change an existing dietary profile, provide the new complete profile and `confirm_profile_change: true`. Every decision includes the constitution snapshot digest as well as its version.

## Verification

```powershell
uv run pytest
uv run ruff check backend tests
# Dedicated disposable PostgreSQL database only; tests create/drop its tables.
$env:CHEF_TEST_POSTGRES_URL='postgresql+psycopg://chef:local-development-only@127.0.0.1:56432/chef_test'
uv run pytest -m postgres
```

Portable tests use SQLite to exercise workflow and policies; they do not prove pgvector SQL works. PostgreSQL tests are skipped explicitly if no dedicated test database is supplied. PostgreSQL must have pgvector available and the migration role must be permitted to enable it.

If the operating-system temp directory is restricted, first create `.test-tmp`, then pass a new project-local path such as `--basetemp=.test-tmp/run1`. Do not use a directory containing real data: pytest owns and may clean its base-temp directory.

See [updated Hebrew plan](docs/IMPLEMENTATION_PLAN_HE.md), [architecture and limits](docs/architecture.md), [operations](docs/OPERATIONS.md), and [verification status](docs/IMPLEMENTATION_STATUS.md).

Culinary family engine, source editor and API: [guide](docs/CULINARY_ENGINE.md).

Kitchen setup and focused cooking interface: [UX and verification](docs/KITCHEN_UX.md).

Clickable local decisions and contextual problem treatments: [rule format](docs/CONTEXTUAL_PROBLEMS.md).

Structured Obsidian Culinary-Knowledge ontology (`vault/Culinary-Knowledge/`, 53 nodes, 118 graph edges, 6 verified sources, 6 decision rules) and engine bridge (`/v1/ontology/summary`, `/v1/ontology/nodes`, `/v1/ontology/diagnose`, `/v1/ontology/sync-dashboard`, `/v1/ontology/export-draft`): see `vault/Culinary-Knowledge/Dashboard.md` and `vault/Culinary-Knowledge/00_Ontology/Chef-Engine-Integration.md`.
