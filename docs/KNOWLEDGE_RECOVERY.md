# Knowledge review and recovery

This milestone implements seven steps before executing checks:
1. Owner-scoped source revision history.
2. Plain-text differences between two revisions of the same source.
3. Reviewer-authorized retirement without erasing historical evidence.
4. Rollback to previously approved knowledge, with fresh policy gates and local vector rebuilding.
5. Authenticated API endpoints and optimistic active-pointer preconditions.
6. Regression cases covering recovery, permissions, stale operations and failed gates.
7. Operating instructions and requirement coverage updates.

Use reviewer authentication for all endpoints. Paths identify a **revision UUID**, not a source slug.

| Request | Purpose |
| --- | --- |
| GET `/v1/knowledge/{revision_id}/revisions` | All revisions of that source and its current active pointer |
| GET `/v1/knowledge/{revision_id}/diff/{other_id}` | Unified Markdown diff from other revision to selected revision |
| POST `/v1/knowledge/{revision_id}/retire` | Remove exactly the currently active revision from retrieval |
| POST `/v1/knowledge/{revision_id}/rollback` | Reactivate a superseded or retired, previously approved revision |

Lifecycle POST body:
```json
{"expected_active_revision_id":"current-active-revision-uuid","reason":"Reviewed reason for this action"}
```
If no revision is active, explicitly use `null` for `expected_active_revision_id`. A stale pointer returns HTTP 409. Reload history before deciding again; never retry with an assumed pointer. Rollback cannot activate a pending or rejected draft. A new approval or lifecycle operation serializes on the source row in PostgreSQL. Gate/vector failures preserve the previous active knowledge; failures do not authorize an older revision by themselves.

Retirement does not delete Markdown, revisions, index history, audit events or cooking citations. Vault synchronization does not reactivate retired knowledge. A genuinely edited file creates a new pending revision requiring review. Rolling back changes active retrieval, not the content of the current Vault file. This is intentional: sync is import-only, so the reviewer should separately reconcile the Vault if desired.

Diffs contain private source material and must be treated as text, never inserted into HTML without escaping. History currently returns the full source revision list; pagination remains future work. No live culinary source is retired or rolled back merely to test these endpoints: regression tests use isolated fixtures.
