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
