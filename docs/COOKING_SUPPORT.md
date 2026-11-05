# Dish interview and structured operations

Implemented 2026-10-26 in the existing cooking workbench, alongside the salmon and gizzard guides.

Start with a dish name, or choose **עוד אין מנה — נבחר לפי משפחה**. The guidance area combines three routes: request a recipe/reference, provide family-level preparation advice, and list the information and knowledge that remain missing. The interview supports meat -> chicken/turkey/beef/other, fish, vegetables, grains/pasta, legumes, eggs, soups/stews and other. It asks for the main ingredients, cut, amount/units, desired result, equipment and method as needed. Each missing detail includes its purpose.

A family-matched Good Food search link helps the cook find a reference. It is a search aid, not a fetched or approved recipe. User recipe text and web links are saved as unreviewed reference material; text is never executed as application instructions. Automatic web fetching and automatic conversion of arbitrary recipes to cooking plans remain outside this change.

The operation picker provides search and category filtering over twelve authored operations: organizing, measuring, cutting, seasoning, boiling, simmering, pan browning, oven cooking, texture checking, temperature measurement, sauce consistency and serving preparation. Selecting an operation shows instructions, checks and explicit observation buttons. Reports send stable operation/outcome IDs and use server-owned responses without model interpretation. Heating operations require a known family and compatible method. Unknown operations can be recorded as knowledge gaps, with the material needed to add a useful rule.

Selection and reports do not complete recipe steps, fabricate measurements, start timers or certify food safety. A free-text custom step remains free text. There is no claim to cover every possible culinary operation. Changing reported dish details clears prior measurements and operation selection. Existing ingredient lists and the original dish title remain intact.

State is stored in the existing journey JSON: `intake_facts`, derived `intake_guidance`, `selected_operation_id`, derived `operation_catalog`, the latest 50 `operation_events`, and up to 30 `operation_gaps`. Signed-in resume reconstructs context with reported classification and refreshes both derived views. Guest sessions use existing browser-local persistence. Unsaved intake drafts survive in-page reports; only saved facts survive a reload. No database migration is needed.

API commands on the existing preview/events routes:

- `intake` with `intake_facts`: full replacement of the interview facts. `family`, `protein`, `goal` and `equipment` are bounded choices; `main_ingredient`, `cut`, `quantity`, `recipe_text` are bounded text. A recipe URL must be HTTP(S) without credentials. An explicitly blank `method` allows clearing the current method.
- `select_operation` with `operation_id`.
- `report_operation` with the selected `operation_id` and an allowed `outcome_id`.
- `request_operation` with `step_title` and optional `message` describing the gap.

Existing revision, ownership, pause and hazard gates apply. Client-provided operation descriptions are never used to generate the response.

Verification: `tests/test_cooking_support.py` covers interviews, recipe reference handling, all catalog outcomes, invalid/stale choices, measurement behavior, paused sessions, knowledge gaps, strict schema round trips and owner-scoped persistence. Run `scripts/check_cooking_support_browser.py` for the complete browser interview/report/reload flow and responsive overflow checks. The existing kitchen-focus browser regression also covers the retained workbench. The two pre-existing ontology tests expecting exactly six sources/rules still disagree with the expanded local vault.
