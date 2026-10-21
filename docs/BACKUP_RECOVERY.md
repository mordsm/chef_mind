# Logical backup and isolated recovery

Seven implementation steps precede checks in this milestone: manifest, database snapshot, Markdown Vault snapshot, guarded restore, operator CLI, regression cases, and operating instructions.

Run from `C:\workspace\chef_mind` with `PYTHONPATH=backend`. Install the locked environment first. These tools are local administrator operations, not API endpoints: a backup includes **all owners' private source and cooking records**. Keep archives in private storage, separate from credentials. Archives are not encrypted and must never be published or committed. The existing `backups/` ignore rule protects that folder from Git; it does not encrypt anything.

## Create and inspect

```powershell
$env:PYTHONPATH='backend'
New-Item -ItemType Directory -Path backups -Force
.\.venv\Scripts\python.exe scripts/backup_local.py create backups/chef-snapshot.zip
.\.venv\Scripts\python.exe scripts/backup_local.py verify backups/chef-snapshot.zip
```

Choose a fresh archive name each time; existing files are never overwritten. No credentials, connection URLs, `.env`, or non-Markdown assets are deliberately collected. Credentials written inside Markdown or cooking records would still be included: keep secrets out of application content. Database rows include immutable revisions, active pointers, vectors, import keys, cooking state and audit history. The constitution snapshot is included with a digest. Manifest SHA-256 checks detect accidental corruption; they do **not** authenticate an archive against malicious replacement. Restore only trusted archives.

PostgreSQL tables are read in one REPEATABLE READ transaction. Vault files are copied separately, with per-file change detection. Pause Vault editing/import and approval activity for a coordinated database/Vault recovery point. This is not an atomic snapshot across the database and filesystem. Historical database revisions remain authoritative for existing citations even when current Markdown differs. SQLite backups are a developer adapter; they do not prove PostgreSQL consistency semantics.

The logical tool caps rows at 100,000, uncompressed archive content at 128 MiB, individual Markdown at 256 KiB and total archive entries near 2,000. For large deployments use native `pg_dump` plus a coordinated Vault copy, deployed code and constitution versions. Logical archives target application schema `0001`; schema evolution requires updating the format/restore compatibility deliberately. Archive checks and row limits are operational bounds, not an untrusted-file sandbox.

## Restore to an isolated target

Prepare a **new empty database** with pgvector and migrate it to the matching application schema. PostgreSQL names must end in `_restore` or `_test`; SQLite filenames must end in `_restore.sqlite`. Never set the ordinary API process to a test database. Set `CHEF_DATABASE_URL` only in the recovery command's environment. This tool never creates or drops database schemas or tables.

```powershell
# Example recovery-only SQLite target; not a production/PostgreSQL substitute.
$env:CHEF_DATABASE_URL='sqlite+pysqlite:///C:/workspace/chef_mind/backups/drill_restore.sqlite'
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\python.exe scripts/backup_local.py restore backups/chef-snapshot.zip --vault-target C:/workspace/chef_mind/backups/vault_restore
Remove-Item Env:CHEF_DATABASE_URL
```

The Vault target must not exist, its parent must exist, and its name must end in `_restore`. Restore validates checksums and schema, refuses nonempty application tables, and inserts all database rows in one transaction. Original source/revision UUIDs and vector data are preserved. No model requests or new approvals occur during restore. Run readiness and a source-grounded answer against the isolated recovered service before choosing any manual cutover.

Database insertion and filesystem writes are not a distributed transaction. If a filesystem write or database commit fails, the database transaction rolls back where possible, but a partial recovery directory can remain for inspection. The tool never automatically deletes or overwrites such a directory. Retry with a fresh recovery target after diagnosing the failure. Keep the production service unchanged until the recovered system has been checked; cutover and destructive cleanup require a separate operator decision.
