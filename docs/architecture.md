# Chef Core — implemented first slice

Constitution content version 0.1, received 2026-10-19. The source snapshot and digest are in CHEF_CONSTITUTION_0_1.md. The implementation plan amendment takes precedence over its historical “missing constitution” intake notes.

One FastAPI service owns API authentication, review, retrieval and decisions. PostgreSQL stores immutable source revisions, indexed units, audit records and cooking state. pgvector stores 384-dimensional vectors; PostgreSQL simple-configuration full-text search and cosine similarity rank candidates. Both the SQL query and result construction require active revisions belonging to the authenticated user. User input never chooses another principal.

The initial engine is **extractive**, not an LLM: it returns reviewed action/reason/observation fields, with explicit source/revision/unit citations. Local character-hash vectors are a deterministic engineering baseline, not multilingual semantic embeddings or a professionally validated chef. Lexical overlap is mandatory, so vector collisions alone do not justify an answer. Model adapters and semantic retrieval quality work remain future tasks.

Approval is synchronous and bounded to 30 units from a 256 KiB file. Under a source lock the service rechecks the latest revision, license and declared conflicts, creates local embeddings, runs the deterministic policy/candidate gate and activates the complete revision in one database transaction. No external model calls hold this transaction open. On failure the old active revision remains. The gate is a limited regression sample plus explicit unsafe-action checks; it does not certify culinary correctness. Human review remains necessary.

Source paths are relative to `vault/<authenticated-user-id>/`. Root containment follows resolved paths, so traversal and outward symlinks cannot import another user's files. YAML uses safe parsing; body Markdown is retained as provenance, not executed or promoted into policy. Only structured frontmatter units enter the first-slice index; automated prose-to-unit extraction is deferred.

Per-user cooking records use optimistic revisions. Records retain original goal, latest reported cooking state, caller-supplied profile/inventory and the last decision. Facts are reported by the caller, not verified by sensors. Omitting the profile on later requests preserves stored dietary constraints; changing them requires `confirm_profile_change=true`. There is no separate profile management service yet. No automatic skill learning or timers are implemented.

Pending revisions and deletions on disk never silently replace active records. This first slice uses explicit API import. Watchers, scan scheduling, removal approval and rollback endpoints are next-cycle work; the database preserves historical revisions needed for them. There is no UI, microphone, vision, appliance control, cloud deployment or change to the Cook Pilot app.

API response confidence is capped at 75 for this baseline and is not a probability or safety assurance. Missing source support, applicability conditions, ingredient quantities or allergy/product data cause clarification or abstention. Exceptions in a free-form source require explicit review rather than being assumed false. Safety readiness is not inferred from elapsed time or color. Cooking advice is never silently substituted for a mandatory safety rule.

Technical references consulted: [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/first-steps/), [SQLAlchemy type variants](https://docs.sqlalchemy.org/en/21/core/type_basics.html), [pgvector Python integration](https://github.com/pgvector/pgvector-python). The dependency versions actually resolved for this checkout are pinned in uv.lock.
