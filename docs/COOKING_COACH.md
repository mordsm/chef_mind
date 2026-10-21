# Cooking Coach

The primary console is now a three-area cooking workspace: journey, chef companion, and contextual learning. The original knowledge-review tools and general source-grounded advisor remain available, with pantry/settings collapsed by default.

## User-directed work (default)

Structured questions use the local decision table in `app/decision_table.py`.
Options display their labels without numbers. Click an option to answer;
Enter sends typed text, Shift+Enter inserts a newline. Explicit
choices are stored in the journey, acknowledged immediately, and answered
questions disappear. Gizzard questions cover ingredient condition, method and
desired result. The exact phrase `תבשיל רך ברוטב` is also recognized without a
model. Other free text still uses the bounded local dialogue rules; this is not
general natural-language understanding. Choosing an option never certifies
safety, supplies a measurement, or completes a cooking step.

The knowledge catalog shows each document's original reference, attribution,
tags, adaptation notes and review status. BCcampus custard and connective-tissue
entries are supplemental documents for the advanced source-retrieval advisor;
they are separate from the two YAML graphs and from the active cooking recipe.

Use **המלאי שלי — צפייה, הוספה ועדכון** above the workspace to open the inventory
editor inside **המלאי שלי, התאמות ומקורות**. Quantity, unit and ingredient name
are editable. Guest inventory stays in this browser; connect to recover private
server inventory. A restored journey is explicitly labelled as previous work.
Starting over before any action/report does not ask to replace an untouched plan;
an existing plan with progress still requires confirmation.

Gizzards are recognized as `קורקבנים` and `קוקבנים` as well as English aliases.
Startup shows preparation guidance, the separate poultry safety check, and
questions about ingredient condition, cooking method and desired result. The
questions remain visible beside the conversation input.

Enter any dish, optionally choose a method and ingredients, and select Mentor or Consultant. The system starts an empty, user-owned checklist, not an imposed recipe. Eight reusable dish families currently cover poultry/turkey, fish, meat, eggs, pasta, grains, vegetables, and soups/stews. Unknown dishes receive explicit general guidance and clarification questions. Turkey wings also have specific roast/simmer alternatives linked to the manufacturer's guidance; no universal cooking time is invented.

The cook can add, edit, reorder, select, and remove actions, accept suggestions individually, report progress, request help, and end work. Reports and advice never insert actions or mark them complete. Completing an action records the user's statement and does not certify safety. Ending work opens a debrief based on reported issues and measurements, including unresolved/missing safety information. Editing dish details retains the user's checklist and original title, refreshes context, and invalidates earlier temperature assessment.

Mentor check-ins follow five minutes without a user update; Consultant uses ten minutes. Manual reminder expiry is separate. Both are deduplicated, ask for observations, and never advance the checklist. Captured temperatures come only from the explicit measurement field, not incidental numbers or negated statements in free text. Proactive re-renders retain unsent report, new-action, and temperature drafts.

Mentor/consultant mode and chef style appear above the dish fields. The current
action card includes the latest chef response, applicable guidance and safety
checks alongside the action. On narrow screens these stay together inside the
same card. Background material remains in the learning area, and conversation
history stays collapsed. The original authored journeys remain optional examples.

Additional events: `start_custom`, `update_plan`, `report`, `add_step`, `edit_step`, `remove_step`, `move_step`, `select_step`, `mode`, and `finish`. User-authored action instructions are marked `USER_PROVIDED`, not attributed to a published source. Contextual knowledge and editorial recovery rules are kept separate.

## Working behavior

- Three authored starter journeys: shakshuka, tomato pasta, and oven chicken. They are instructional starters, not professionally kitchen-tested recipes. General questions and other dishes retain the existing approved-knowledge path.
- Smart steps include instruction, why, common mistakes, success criteria, questions, failures, recovery, answer choices, check-in timing, and source. Learning is short and changes with the current step.
- A reported successful state enables completion. Pressing Done without a successful observation asks the status question; time alone never completes a step. A subsequent failure invalidates earlier success.
- Chicken readiness requires a user-reported measured temperature of at least 74°C, following FoodSafety.gov. Personality changes tone, not thresholds or advancement rules.
- Timer expiry and three minutes without a user update trigger separate, deduplicated check-ins. Pause freezes the reminder; resume rebases its deadline. Pausing does not operate cooking equipment. Background/browser throttling can delay notifications.
- Supportive, professional, and direct/tough styles are saved in journey state. Questions about why, current-stage troubleshooting, and recovery are handled by the local step workflow; this is not unrestricted model-generated culinary advice.
- Explicitly reported fire hazards pause coaching and require confirmation that the hazard has been resolved before resuming. Known egg/wheat avoidance conflicts block the relevant starter; empty metadata does not certify allergen absence.

## Persistence and connection

Guest cooking starts without a token. Its journey and ingredient selections persist in this browser, under guest-specific keys. It never exposes authenticated inventories. Connect to recover private inventory and the most recent private journey. Tokens remain in tab memory; a page reload requires reconnecting for private data.

Authenticated journeys use owner-scoped `CookingRecord` snapshots with optimistic revisions and a row lock. `COACH_EVENT` audit entries record actions. No database migration is needed. Wrong-journey and stale-revision updates return conflicts instead of modifying a different session. Guest preview requests do not create private records.

The pantry has two/three cards per row and ingredient buttons with quantity badges. Each click increases the quantity in that ingredient's current unit. Server inventory timestamps are UTC; a marked dirty local edit can survive a failed save. Legacy empty browser copies no longer automatically overwrite recovered inventories. A history selector explicitly restores earlier cooking inventory. Guest inventory and private inventory are separate.

## Voice and photos

Optional **הקלדה בקול** replaces typing; it is not a conversation mode. Each
question/report field has its own microphone button, so there is no target
selector. Text is inserted without being sent automatically. Continuous browser
recognition retries up to twice after an unexpected end; ordinary guidance
updates do not stop it. Permission, microphone and network failures receive
specific messages rather than a silent close. HTTPS/localhost and browser support
are required. Speech services may process audio remotely; no OpenAI call is made.
Stopping, hiding the page or resetting stops capture. Read-aloud remains inside
the optional voice tools and prefers a matching local voice.

Photo attachment accepts JPEG/PNG/WebP up to 8MB, creates a local preview, and explicitly states that image analysis is unavailable. No image is uploaded or interpreted. Users can describe the image in their question. Do not claim visual observations from this preview.

## API

| Endpoint | Access | Function |
|---|---|---|
| `GET /v1/coach/recipes` | Public | Authored starter smart-step definitions |
| `POST /v1/coach/preview` | Public | Validate/apply one guest event without persistence |
| `GET /v1/coach/current` | Authenticated | Most recent owner-scoped journey |
| `POST /v1/coach/events` | Authenticated | Persist validated state transitions |
| `GET /v1/inventory/history` | Authenticated | Up to 30 earlier inventories from 500 recent decision events |

Events: start, answer, complete, problem, ask, timer, pause, resume, check_in, personality. Private updates include `journey_id` and `expected_revision`.

## Verification

`tests/test_coach.py` checks validation, timer/idle behavior, recovery, pause/resume, temperature gates, allergy conflicts, safety holds, completion, owner isolation, revisions, and guest privacy. `scripts/check_coach_browser.py` drives the complete UI in Edge against the actual FastAPI workflow and isolated SQLite storage, including recovery from old empty browser inventory, guest/private persistence, no-randomUUID compatibility, and 1440/900/390px widths. Speech APIs are mocked in automation; this does not prove physical microphone/audio behavior on a user's device. `scripts/check_console_browser.py` retains independent regression coverage of legacy controls.

Sources checked 2026-10-19: [FoodSafety.gov temperature guidance](https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures) and [CIA cooking-method background](https://www.ciachef.edu/blog/3-types-cooking-methods-foods-love/). Starter check-in intervals are authored estimates, not source-verified cooking durations.
