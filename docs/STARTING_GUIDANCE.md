# Starting guidance and inventory usability

Seven implementation steps before checks: explain optional reports, allow an initial question without fabricated observations, expose approved-topic scope and explicit condition prompts, show loading/focus responses, consolidate ingredient rows, add backend/browser regressions, and document behavior.

## What to enter before cooking

Enter what you want to prepare and the ingredients/quantities available. The question field can be empty: the browser sends a request asking how to start the entered goal. Reports are optional and remain empty until something actually happened. For example, later reports might be “I chopped the onion” or “the sauce is still thin.” A condition is a factual precondition of a source technique. Clarification responses expose unmet conditions as unchecked confirmation boxes; the user must explicitly confirm those facts. Editing the goal or question unchecks these confirmations. No completion, measurement or condition is invented from silence.

## What “insufficient approved knowledge” means

The current corpus contains six topic-specific units, not a complete recipe database. Supplying an OpenAI key does not expand the approved corpus: the model selects among approved units and cannot silently replace them with generated recipes. A dish outside this coverage can still return insufficient evidence. The revised response explains this limitation, shows a small owner-scoped list of approved topics and states that a suitable source must be reviewed before full guidance is available. Draft/rejected/retired sources and other owners' sources are not exposed as suggestions. Topic buttons change the visible goal; they do not trigger an API call or confirm a technique's conditions.

## Visible submission and compact inventory

The submit button shows a loading label and disables repeated submissions while awaiting the request. The page shows a sent status and focuses/scrolls to the response when ready, including clarification or insufficient-evidence responses. Native invalid inputs show an explanatory status instead of appearing to do nothing. Result focus does not submit another request or invoke speech.

Ingredient name, quantity, unit, classification, availability confirmation, label confirmation, allergens and removal are arranged in one row on wide desktops. Narrow screens wrap the same fields to keep them readable. Integer/decimal quantities retain their existing numeric behavior. “Availability verified” means the displayed quantity/availability has been checked; unchecked is uncertainty, not definite absence. Conditions are confirmed separately from ingredients.

The console remains a bounded Chef Core prototype. This change improves the starting flow and error explanation; it does not claim complete recipe discovery, extraction or general culinary coverage. No new knowledge is automatically approved.
