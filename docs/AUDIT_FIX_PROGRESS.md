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

## Cycle 5 — bounded cold-salad pilot (completed 2026-11-06)

CM-003/005/006, limited to a declared raw-vegetable salad: after ingredients,
quantity and equipment are provided, create four editorial steps without manual
step authoring. Each step has an instruction and observable completion check.
Only explicit user confirmation advances it. Unknown mixtures, heated methods
and animal ingredients do not enter this cold pilot. This is not a complete
recipe generator for arbitrary dishes.

Store reported problems and missing ingredients separately across side questions
and refresh. An explicit supported reminder request starts the existing actual
deadline/check-in mechanism. Invalid, negated or unbounded requests do not start
a timer. Live mode keeps the current action visible and puts the full six-block
protocol inside a closed expandable section. Pilot instructions are marked as
editorial; the FDA produce source supports handling background, not recipe
validation. Fixed reminder check-in idempotence discovered by regression tests.
The final UI review also preserves plain dietary/composition rejection messages
in guest and authenticated requests instead of reducing them to a generic error.

Final validation: full Python suite 324 passed / 4 skipped; 25 focused tests
passed after the last memory/timer parsing changes; six Node tests passed.
Desktop/mobile station and Obsidian export checks passed. The real HTTP/PWA
journal check passed, including two-device conflict handling and offline reload,
after correcting the test's asynchronous-save wait. New pilot modules and replay
harness pass Ruff. The old broad coach browser harness has obsolete selectors
and removed custom-step controls; its failure is not reported as a passing run.
Built-in shakshuka is instead covered by the bounded replay browser check.
That replay browser check passed at 1440/390 widths, including explicit step
confirmation, visible dietary/composition messages, a real two-second deadline,
refresh memory, and preservation of a typed question after an unavailable API.

All six original dialogue inputs were replayed against isolated model-disabled
code. Only salad creates a full plan (four steps); beef, fish, legumes, soup and
bread still have zero generated steps. Their timers now start; that alone is not
successful guided cooking. See the Hebrew implementation report for final scope.
Artifacts: C:/workspace/.runtime/chef-audit-rerun-20261106.

Remaining: expand beyond the one-dish pilot; CM-007 embedded reporter loading;
CM-013 live technique-policy verification; authorized live retrieval comparison;
physical voice/cooking checks. No deployment, merge, or blanket source approval.

## User-authorized expansion — five complete dish plans, 2026-11-06

Following the user's request to complete the other dishes, added scoped authored
plans for beef stew (6 steps), oven salmon (4), lentils/vegetables (5), vegetable
soup (5), and yeast bread (5). The plan catalog records sources, timing conditions
and a SHA-256 revision. These are authored adaptations, not blanket approvals of
external recipes. Every step includes a visible instruction and completion check.

Completion gates require reported temperature for the beef/salmon cooking step.
Jumping to serving, deleting the cooking check, or reusing a reading from another
step cannot complete that check. Intake edits invalidate generated quantities,
old completion IDs and timers. Custom user steps are preserved. Finish summaries
use the plan's target rather than a different cut's rest rule.

Specific recovery and substitution replies preserve dish, problem and missing
ingredient context across side questions. Explanatory questions no longer replace
observations in memory. The original salty-soup prompt receives actual dilution
and continued-cooking guidance. The old fish fallback no longer overwrites this
authored oven plan. Intake recognizes the authored plan; the glossary/Obsidian
note now includes 24 plain-language entries.

Scope: matching declared recipe ingredients, family and equipment; no silently
discarded additions, frozen/stuffed/minced fish, or substitution of kidney beans
for lentils. Bread supports 400–540 g dough, not a guaranteed baked loaf weight.
See FULL_DISH_PLANS_HE.md for source conditions, evidence and remaining limits.

Validation: full Python suite 346 passed / 4 skipped. After final memory and
finish-summary corrections, 30 focused plan/salad tests passed. The final
temperature-target hardening additionally uses server catalog values rather than
client-returned step values: 23 focused tests passed, plus two final boundary
cases for a removed/lowered returned target passed. Counts overlap earlier runs.
Six Node gateway/worker tests passed; station/glossary/Obsidian browser acceptance
passed at desktop/mobile widths. The final six original dialogue replays all
produced plans, and all five added plans completed in mobile browser controls.
Real reminder, refresh, unavailable-network input and built-in shakshuka checks
also passed. Final artifacts: C:/workspace/.runtime/chef-full-plans-final-20261106.
No production deployment, merge, physical cooking or real microphone claim.
