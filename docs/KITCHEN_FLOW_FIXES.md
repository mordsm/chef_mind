# Kitchen flow fixes

- Starting a dish proceeds without the replacement confirmation dialog.
- Completing the clean/thawed gizzard choices for simmering opens a three-step plan, rather than leaving the workbench empty.
- A boiling-liquid report receives a simmering response without automatically completing a step.
- The composer groups reports, questions, and adding a personal action. Moved action forms are removed before rendering to prevent duplicate IDs.
- A unique matching knowledge-graph path is adopted after the final explicit setup answer.

Validation: 23 focused pytest tests passed; the kitchen-focus Playwright script passed, including composer switching, plan editing, report failure preservation, timers, responsive layout, salmon choices, and draft persistence. JavaScript syntax checks passed.

## Follow-up: close guidance and visible actions

Personal actions are always visible beneath the report/question composer rather than hidden behind a mode. Existing saved empty gizzard plans recover on the next report, question, or check-in. Boiling reports accept variants and reject negative statements. Responses explicitly describe lowering heat, checking liquid and tenderness, and the next information to report. No recipe duration is invented: the current local sources lack a tested gizzard recipe with weight, cut size, pot/lid, duration range, and check intervals. Such a recipe is the requested additional knowledge source.

Verification: 29 focused tests and the kitchen-focus browser script passed. Restarted the local Chef service to load backend changes; live preview requests verified choices create the plan and a boiling report produces immediate heat guidance.

## User protocol integration — 2026-10-25

Stored the supplied protocol in `backend/app/data/gizzard_user_protocol.json` with stable source ID, user attribution, and `CITATION_NOT_VERIFIED`. Initial preparation and boiling/time/toughness replies now include the conditional 90–120 minute range for 1 kg halved gizzards in a heavy ordinary covered pot. Counting from the gentle simmer is explicitly an implementation assumption; the supplied protocol did not state the clock origin. The first tenderness check is suggested at the beginning of the range; this is an operational choice, not a quoted check schedule. Timers still require an explicit user click.

Pressure-cooker timings, percentage extensions, exact liquid temperatures, and causal absolutes were preserved as unverified source claims and excluded from automatic advice. The protocol is not represented as a verified quotation from Joy of Cooking. No source-review database activation was performed.

Validation: 30 focused tests and the kitchen-focus browser script passed.
