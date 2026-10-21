# Editable culinary YAML sources

The console's **Knowledge → YAML · Knowledge sources** panel lets users load,
edit and save either supplied document, or add individual entries. It supports
Hebrew and English. Original documents load automatically without signing in,
including when switching the source selector. Sign in with a Chef Core token;
a `reviewer` role is required for writes. Private reads and revisions are scoped
to the token's user ID. A private-storage failure falls back visibly to the
read-only original and never presents it as the user's saved draft.

Apply the database migration and restart the service before using the editor:

```powershell
uv run alembic upgrade head
```

Source keys are `graph` (`culinary_graph_source.yaml`) and `domain`
(`culinary_domain_source.yaml`). Revision 0 is the supplied file. Changes are
private, immutable database revisions; the packaged files remain intact.
The existing logical backup includes these revisions. Older schema-0001
backups can still be restored into an empty migrated target.

## API

Use `Authorization: Bearer <Chef Core token>`. Interactive schemas and request
examples are available at `/docs`.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v1/culinary/sources` | List the two sources, revisions and section counts |
| GET | `/v1/culinary/templates/{key}` | Read the public packaged original without authentication or database access |
| GET | `/v1/culinary/sources/{key}` | Read the current YAML |
| GET | `/v1/culinary/sources/{key}?revision=0` | Read the original (any saved revision number also works) |
| PUT | `/v1/culinary/sources/{key}` | Replace the complete YAML |
| POST | `/v1/culinary/sources/{key}/entries` | Add a mapping entry or append a recipe path |

Read the current revision before writing. Full replacement accepts:

```json
{"expected_revision": 0, "yaml_text": "<complete YAML document>"}
```

Add an ingredient to `graph` with:

```json
{
  "expected_revision": 0,
  "section": "base_ingredients",
  "entry_id": "new_vegetable",
  "yaml_text": "name: New vegetable\ncategory: vegetables\nbase_rules: []\n"
}
```

Use an existing section name. For `recipe_paths`, omit `entry_id` and supply a
YAML mapping containing the path and valid `ingredient_ref` and `method_ref`
values, plus `archetype_ref` for the domain document. Paths are appended.
For existing entries, use full-document replacement. New IDs never overwrite
existing ones. A stale `expected_revision` returns HTTP 409; preserve local
edits, reload, then merge and retry. To restore an older document, GET its
revision and PUT that YAML using the **current** expected revision.

YAML is limited to 256 KiB with bounded nesting/complexity, unique string keys,
safe tags, no recursive aliases, the original four sections and valid path
references. Mapping entries remain extensible; this validates document
structure, not culinary accuracy. Full saves preserve comments and anchors;
adding entries normalizes YAML formatting and expands inherited mappings,
while prior revisions preserve the original text.

## Relationship to coaching

These are **source drafts**, not active coaching configuration. Responses
explicitly return `status: source_draft` and `used_by_coach: false`.
The current graph uses hand-curated adaptations in `knowledge_graph.py` and
`culinary_domain.py`, including independent food safety rules. Merely saving
an ingredient, technique or path does not adapt or activate it. Activation of
these graph changes currently requires a reviewed code change; this editor
does not provide a graph-publishing button. Ordinary knowledge documents can
still use the existing Markdown import/review/activation workflow.
