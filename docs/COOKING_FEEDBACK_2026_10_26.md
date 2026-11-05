# Cooking feedback, 2026-10-26

Applied on top of existing local cooking-flow changes:

- Separate book provenance from cooking text; retain source IDs, hashes, page references and validation notes in source metadata.
- Practical vegetable-softening advice includes fork testing, draining and transfer to sauce. It explicitly identifies the suggested procedure as an application of the principle rather than a recipe from the book.
- Explain short cooking versus prolonged tenderizing with concrete cut and texture examples; simplify the brining/marinade explanation.
- Add an explicit progress-check action and concrete criteria to generated gizzard steps. A report never automatically completes a step.
- Place dictation and send side by side, hide duplicate dictation controls in custom cooking, and label playback separately. Keep dictation available in legacy journeys.
- Set explicit dark text and a pale background on quick report buttons.

Existing gizzard and salmon flows provide guided preparation after their supported choices. This change does not implement arbitrary recipe generation. User-authored step text and reports are interpreted through local rules, not unrestricted language understanding or physical observation. Appearance alone cannot verify doneness.

Validation: focused backend regressions, Node syntax checks and the kitchen-focus browser script. The broader suite also exposes two ontology tests with fixed source/rule counts that no longer match the current local vault (21 sources / 24 rules versus expected 6); these unrelated assertions were left unchanged.
