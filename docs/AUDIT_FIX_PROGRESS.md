# Controlled audit fixes — 2026-11-05

Baseline committed and pushed first: `5a766c4` on `master`.
Implementation branch: `fix/controlled-audit-20261105`, in a separate worktree.
No production deployment is authorized by this implementation run.

Baseline verification: 294 tests passed, one skipped and two failed because the
initial command ran outside the project directory. Both path-dependent tests
passed when rerun from the project root. Six Node gateway/worker tests passed.

## Cycle 1 — declared ingredient constraints

CM-001 and CM-010: shared ingredient-name checks cover compound labels, Hebrew
and English aliases, nuts, sesame, fish species and custom avoidances. Checks
run before opening a custom journey, on ingredient/classification updates and
when attaching a recipe. The grounded Chef route uses the same checks.
Known meat/dairy combinations are rejected when that preference is selected;
named plant milks do not automatically count as dairy. Unknown prepared mixtures
with allergies require a label check. These are declared-composition checks,
not a certificate of product labeling, cross-contact or medical suitability.

Validation: 60 focused tests passed, including guest/authenticated API conflicts,
recipe/update bypass attempts, custom avoidance, plant-alternative controls and
existing coach/station regressions. Production remains unchanged; the original
live audit findings are not marked fixed in production.

## Cycle 2 — dried red kidney beans

CM-002: the station checks declared red kidney beans and their stated condition
before ordinary advice. Dried/unspecified cases receive a visible warning, a
state question and the FDA natural-toxins source. Explicit canned/previously
cooked controls do not receive dry-bean instructions. The same station gate
serves coach and grounded responses. This is not confirmation that a user has
actually performed the required preparation.

Validation: 38 safety/station tests passed, including the exact slow-cooker
question from the audit and dry/canned/unknown controls. No live deployment.

## Cycle 3 — visible action and warning

CM-004/011 and presentation part of CM-012: a current-action card precedes the
full station protocol. Contextual answers and warnings no longer go only into
closed science details; safety holds retain priority. Stale learning answers
are cleared on non-dialogue transitions. Restored the two corrupted Hebrew
strings and replaced vague generic seasoning prose with concrete tasting steps.

Browser regression passed at desktop/mobile widths with model recognition
disabled; focused tests additionally cover foreground burning/bean warnings.
This preserves the six-block full protocol and existing source exports.

## Cycle 4 — normalized source references and food relevance

CM-008/009: legacy singular source_id and source-page metadata are normalized
alongside existing source lists. Explanatory summary paragraphs can be retrieved
as background; they are not executed as recipes or approved en masse. Fish/egg
scope and bilingual poaching relevance prevent the reproduced cross-food result.
Retrieved tips carry note ID and SHA-256; the schema preserves those fields.
Exports distinguish editorial references from approved action citations, while
the legacy source_ids field remains a compatibility reference index.

Validation: 38 book/station/ontology tests passed. Initial tests caught Hebrew
ranking and strict-schema issues; both were corrected before committing.
No production private index approval or deployment was performed.
