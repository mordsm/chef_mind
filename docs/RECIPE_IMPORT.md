# Selected recipes and action feedback

Selecting a recipe in another browser tab cannot automatically communicate the
selection back to this application. In preparation, open "צרף מתכון שבחרתי",
paste the URL and choose import. Review the extracted steps and explicitly adopt
them into the cooking plan. Existing plan replacement is named on the approval
button. When a website cannot be read, paste preparation instructions, one step
per line, and review them through the same flow.

URL import reads bounded schema.org Recipe JSON-LD, including nested HowToSection
and HowToStep entries, from the configured recipe publishers only. Redirects are
subject to the same host allowlist. Non-recipe articles are not converted into
instructions. No script or source instruction is executed and no model is called.
The source URL, ingredients and exact imported instructions remain in the recipe
snapshot; imported instructions do not certify food safety or mark steps complete.

Action reports store snapshot and step IDs. Feedback displays the original current
step and an action-specific reminder. A different recognized action raises a
comparison prompt rather than declaring the cook wrong. Unlinked reports clearly
state that their advice is general. The latest saved action is always visible;
the full editable journal is expandable.

Countdowns, including any older general reminder, appear in the reporter's single
timer section. Finishing a timer still does not certify completion or readiness.
