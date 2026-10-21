# Source corpus and model milestone

Seven implementation steps completed before executing tests:

1. Five attributed culinary knowledge drafts and provenance fields.
2. Optional OpenAI Responses structured-selection adapter with verified TLS, timeout and no retries.
3. Model integration with request opt-in, active-source validation and independent policy checks.
4. Owner-isolated, read-only Vault reconciliation with duplicate and malformed-file reporting.
5. Configurable background polling plus manual reconciliation endpoint.
6. Twenty culinary scenarios and a reviewer-only evaluation endpoint.
7. Regression coverage and these operating/review instructions.

## Sources and review dossier

All five new Markdown files are under `vault/owner/00_inbox`. Each contains source URL, attribution, reuse reference and adaptation notes. `verified_on` means source checked on that date, **not** human culinary validation. The drafts remain inactive until a reviewer approves the concrete revision. No proprietary culinary book was imported.

| File | Source | Reuse | Scope |
| --- | --- | --- | --- |
| bccampus-starch.md | [Gelatinization](https://opentextbc.ca/modernpastryandplateddesserts/chapter/gelatinization/) | CC BY 4.0 | Starch slurry |
| bccampus-custard.md | [Coagulation](https://opentextbc.ca/modernpastryandplateddesserts/chapter/coagulation/) | CC BY 4.0 | Overheated custard; stopping heat is an editorial inference |
| bccampus-sugar.md | [Crystallization](https://opentextbc.ca/modernpastryandplateddesserts/chapter/crystallization/) | CC BY 4.0 | Avoid excessive agitation; clean equipment |
| bccampus-meat.md | [Meat Fibres and Tenderness Factors](https://opentextbc.ca/meatcutting/chapter/meat-fibres-and-tenderness-factors/) | CC BY 4.0 | Identify cuts and connective tissue; no cooking schedule |
| usda-thermometer.md | [FSIS Food Thermometers](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers) | Agency text under [USDA reuse policy](https://www.usda.gov/about-usda/policies-and-links) | Probe placement; no claim of measured doneness |

BCcampus author: The BC Cook Articulation Committee, 2015. License: https://creativecommons.org/licenses/by/4.0/. All text is paraphrased/adapted into Hebrew. Images, logos and separately licensed third-party material are excluded. USDA `permission_granted` denotes its published public-domain reuse authorization, not an individual license or endorsement. No source is advertised as error-free: the gelatinization chapter contains inconsistent agar descriptions; agar guidance was deliberately excluded. Meat source images carry noncommercial restrictions and are excluded.

Review the source and every unit's action, conditions, exceptions, allergens, kashrut and safety notes. Use existing `/v1/knowledge/{revision_id}/approve` with expected revision and an honest review reason. Approval runs the existing activation gate atomically. The 20-case culinary suite is an additional release check, not a substitute for human review or a cooking trial.

## Model operation

For a project-local key, put `CHEF_OPENAI_API_KEY=your-key` in `C:\workspace\chef_mind\.env` and restart the API. This key is loaded as a masked secret and passed explicitly to the SDK, taking precedence over an inherited `OPENAI_API_KEY`. `.env` is ignored by Git. Leave the project key empty to use the ambient `OPENAI_API_KEY` instead. Do not paste keys into chat.

Set `CHEF_MODEL_ENABLED=true`, `CHEF_MODEL_NAME=gpt-6-luna` (configurable), and `OPENAI_API_KEY` in the process environment. Each request must additionally set `allow_external_model=true`. Only question, current goal, user-reported observations and candidate source snippets/IDs are sent. No API tokens, owner ID, cooking ID or full inventory is sent. The API is called with `store=false`; this does not promise zero provider retention under every account's data controls.

The model selects one approved source, using [Responses structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses). It does not invent or rewrite the culinary action. [Model documentation](https://developers.openai.com/api/docs/models/gpt-6-luna). Output is checked against the current owner and active source revision, then conditions, required inventory and policies are checked locally. Refusal, timeout and invalid output fall back to the extractive engine with a visible policy flag. No transaction/row lock spans the external call. Live API availability and subjective cooking quality require a separate opt-in evaluation; offline mocks do not establish these.

## Vault operation

Set `CHEF_SYNC_ENABLED=true` and `CHEF_POLL_SECONDS=10`, then restart the API. Run one worker per Vault/database deployment. Polling imports changes only into pending review. Alternatively a reviewer may POST `/v1/vault/sync`. Stable `source_id` preserves identity across moves. Duplicate IDs are rejected. Missing files are reported and active knowledge retained; there is no automatic deletion or rollback UI. Malformed files do not stop other imports. Scans cap file count at 1000 and each document at 256 KiB. Use a dedicated culinary Vault namespace: unrelated Markdown is reported as invalid.

POST `/v1/evaluations/culinary` after approving these five drafts. Results expose each expected/actual decision and action citation IDs. An empty corpus should fail this suite rather than masquerade as a validated release.
