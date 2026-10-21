# Operations for the first slice

Start in the repository root. Install locked dependencies, configure private API tokens, start PostgreSQL/pgvector and run Alembic before starting FastAPI. Bind to loopback for the local pilot. Compose also includes an API container; pass a real private `CHEF_API_KEYS` map through the environment before starting it. Obsidian is optional and never runs inside the service.

`python scripts/bootstrap_local.py` creates ignored `.env` once with a random owner token, or preserves the existing file. Use `docker compose --env-file .env -p chef-mind -f infra/docker-compose.yml ...` so Compose reads the root configuration. The current database port is 56432 and API port is 8800. Do not paste tokens into shared logs or issue trackers.

Schema migration: `uv run alembic upgrade head` with `PYTHONPATH=backend`. Do not point tests at a real user database. The optional PostgreSQL test fixture explicitly requires a database name ending in `_test` and drops/recreates its tables. No migrations or resets run automatically during ordinary API startup.

Knowledge activation is explicit and synchronous. Rejected, unlicensed, conflicting or regression-failing candidates cannot replace active knowledge. After editing a Markdown file, import again with a new idempotency key, inspect the new pending revision and approve its exact revision number. Reusing a key for changed content returns 409. Retry a failed local transaction after inspecting state; never assume activation succeeded from a timeout alone. The query/review APIs show the actual status.

For backups, use the bounded logical archive tool in [Backup recovery](BACKUP_RECOVERY.md), or PostgreSQL `pg_dump` and a coordinated copy of `vault/` plus deployed application/constitution versions for larger deployments. Keep credentials separate. Restore into a new database with pgvector installed and run readiness and source-grounded answer checks before use. Do not overwrite a running database or delete Docker volumes as a routine setup step.

SQLite is a test/developer adapter only. It permits local workflow verification when Docker is unavailable but cannot establish PostgreSQL vector indexing correctness. Record PostgreSQL coverage and unavailable infrastructure explicitly.

Optional OpenAI source selection and local Vault polling are configured separately; external model requests still require per-request opt-in. Cloud Vault synchronization, public deployment and automatic lesson retention are not enabled. User state is per API-token principal and cooking ID. Avoid reusing a principal between unrelated users. Source review requires `reviewer`; cooking-only tokens cannot import or approve. Store tokens in `.env` or the process environment, never in the Vault, logs or Git.
