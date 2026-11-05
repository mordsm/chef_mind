# Chef Mind — user-facing language

Write cooking instructions in everyday Hebrew. Give a concrete action before
background: what to do, with which tool, a supported amount or time estimate,
what to check, and when to stop. Seasoning instructions must also be actionable.

Do not use expert shorthand as an instruction. Prefer "add a small pinch of salt,
stir and taste" over "balance salinity". If a step is unnecessary for the chosen
preparation, say so directly instead of exposing an internal evidence disclaimer.
Keep safety-critical actions visible and background explanations expandable.

When a technical term is necessary, add a short plain-language definition to
`backend/app/static/culinary-glossary.js` and regenerate its Obsidian note with
`node scripts/export_culinary_glossary.cjs`. Do not assume the dictionary knows
every new term. Preserve keyboard access and focus restoration for explanations.

Distinguish planning-time estimates from measured cooking completion. Record
the source and conditions of time estimates; do not invent precise timing or
apply a table from one liquid temperature as a validated recipe at another.

When asked to save a guide to the vault, create an actual source note; a UI link
alone is insufficient. Clearly distinguish summaries from complete local copies,
and vault storage from approval/activation in the decision index.

See `docs/PLAIN_LANGUAGE_GUIDANCE.md` for the workflow and current source notes.
