# Culinary decision graph integration

The user-supplied production graph is archived verbatim in
`backend/app/data/culinary_graph_source.yaml`. `app.knowledge_graph` computes its
SHA-256 and validates all references on load: 75 ingredients, 5 preparations,
10 cooking methods and 20 optional recipe paths.

The active graph is an editorial adaptation, not a professionally validated
knowledge source. Ingredient advice, method advice and observations retain
source IDs pointing into the archived document. They are labelled as adapted
user knowledge in the interface. The original recipe timings and low-temperature
processes are not executed. Raw/cured and sous-vide paths remain unavailable
pending process validation; ambiguous ingredient names request clarification.

Ingredient matching uses aliases, word boundaries, longest matches and explicit
negations. Context comes from the dish name, reported ingredients and selected
method. Reports never stand in for sensors. Only explicit observations trigger
method rules; hazardous observations pause coaching until the user confirms
resolution. Ingredient suggestions never modify the user's checklist. Adopting
a relevant available path requires an explicit action and adds editable macro
steps. Avoidance profiles and meat/dairy separation filter these paths.

Safety minima are independent of original texture targets. Whole beef/lamb cuts
also carry a separate rest requirement; measured core temperature and reported
rest are stored separately and invalidated when the dish changes. Finishing a
session is not a readiness approval. A single temperature cannot validate a raw
or sous-vide process.

Policy references checked 2026-10-19:

- https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures
- https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-fresh-and-frozen-seafood-safely

Public `GET /v1/coach/graph/catalog` exposes adapted nodes, methods and paths.
Authenticated `GET /v1/coach/graph/audit` exposes the original checksum and the
29 original safety fields alongside their independent policy replacements.
`culinary_graph_audit.json` is a reproducible snapshot of that audit. No database
migration or external AI request is required.

The second supplied graph is archived verbatim as
`backend/app/data/culinary_domain_source.yaml`. `app.culinary_domain` retains
16 explicit archetypes and the inheritance of 23 ingredient definitions,
including per-ingredient overrides in the original archive. Two alternate IDs
(sea bass and chickpeas) map to existing nodes, preserving 75 unique ingredients.
The 20 overlapping paths are merged by ingredient and method instead of being
duplicated. Their 80 original actions are individually adapted into editable
steps with explanation, checks, mistakes, recovery prompts and next-step
preparation. Original sensory claims are not treated as safety validation;
original times and temperature targets remain archived. Generic inherited
advice is scoped by ingredient family and never overwrites safety policy.
