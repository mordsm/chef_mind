# Culinary Knowledge Engine

The standalone engine lives in `culinary_engine/`. Its UTF-8 source files are
`config/culinary_rules_engine.yaml` (families, methods and failure reasons) and
`config/ingredients_registry.yaml` (ingredients and their family).
The initial rules are the owner-supplied culinary heuristics, editable in source;
they are not independently verified scientific claims.

In Chef, open **מאגר הידע → מנוע קולינרי — משפחות וחומרי גלם**.
Everyone can read sources; a reviewer can save shared changes after checking the
explicit shared-change confirmation. Unknown references, duplicate keys, aliases,
contradictory method lists and invalid ingredient mappings are rejected before
writing. Writes replace one source atomically; revision hashes reject stale edits.
Back up these two source files separately from database backups.

Registry ingredients take priority over the legacy family defaults. Approved
per-account method policies retain priority over shared defaults. Adding an
ingredient makes its full display name and its identifier (underscores replaced
by spaces) available for matching dish names and ingredient text. Gizzard spelling
aliases are supported. Methods not explicitly allowed are blocked. Raw curing and
sous vide compatibility does not approve a validated process; these are excluded
from the ordinary Chef method dropdown until such a process exists.

Public API:

- `GET /v1/culinary/engine`: both raw documents, relative source paths and revision.
- `GET /v1/culinary/engine/ingredients/chicken_gizzard/methods`: compatibility list.
- `POST /v1/culinary/engine/validate` with
  `{"ingredient_key":"chicken_gizzard","method_key":"oven_roast_dry"}`:
  `allowed: false`, `error_code: ERR_COLLAGEN_DRY`, explanation and alternatives.

Reviewer API (existing bearer authentication):

- `PUT /v1/culinary/engine/sources/rules` or `/registry` with
  `expected_revision` from GET, `yaml_text`, and `reviewed: true`.
- `PUT /v1/culinary/engine/ingredients/beef_tongue` with `expected_revision`,
  `name: "לשון בקר"`, `archetype: "dense_collagen_lean"`, `reviewed: true`.

These endpoints update shared files, not private drafts. No arbitrary path is accepted.
Run one application worker for serialized source editing; the lock is process-local.
External file edits should not run concurrently with API editing.

Standalone Python API:

```python
from culinary_engine.src.config_manager import ConfigManager
from culinary_engine.src.sous_chef import SousChefEngine

config = ConfigManager()  # or a custom config directory
chef = SousChefEngine(config)
print(config.get_raw_rules_yaml())
print(chef.validate_method_choice("chicken_gizzard", "oven_roast_dry"))
config.add_or_update_ingredient("beef_tongue", "לשון בקר", "dense_collagen_lean")
print(chef.get_allowed_methods("beef_tongue"))
```

`config.reload()` validates and reloads both sources. The existing engine object
uses the updated configuration. Raw saves preserve source text, including comments.
The structured ingredient API serializes the registry and does not preserve comments.

Demo: from the project root, run `.venv\Scripts\python.exe culinary_engine\main.py`.
It prints the registry, verifies the gizzard exclusion and error code, and **adds
beef_tongue to the source registry**. Use `--config-dir PATH` with a copied config
directory to demonstrate persistence without changing shared defaults.
