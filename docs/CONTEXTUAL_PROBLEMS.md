# Local choices and contextual problem rules

All structured question buttons send `action: answer`, `question_id` and `answer`
to Chef. Decision tables and problem rules select the reply locally. These paths
do not call a language model. Choosing a goal records it without silently adding
or changing cooking steps. Only one unanswered question is shown at a time.

Problem responses live in `backend/app/data/problem_rules.yaml`. The Knowledge
page's **כללי טיפול בבעיות** editor and `/v1/coach/problem-rules` API support private,
reviewer-approved versions. Existing private versions remain full overrides;
they do not silently inherit newly added shared rules. In the editor, press
**הוסף טיפולים חסרים מברירת המחדל לטיוטה**, review, and save to activate additions.
The preview endpoint `POST /v1/coach/problem-rules/with-defaults` accepts
`yaml_text`, fills absent problem IDs and preserves existing rules and unsaved
edits. It makes no persistent changes. Existing generic responses are not
silently replaced by contextual ones.

A basic rule may retain its existing `response` and optional `methods`. A
conditional rule can add `questions` and `variants`:

```yaml
rules:
  too_dry:
    questions:
      - id: dry_state
        text: מה בדיוק יבש במנה?
        options:
          - {id: liquid_low, label: הנוזל בסיר כמעט נגמר}
          - {id: cooked_dry, label: כבר בושל אבל יבש באכילה}
    variants:
      - id: gizzard_liquid_low
        dish_terms: [קורקבנים, קוקבנים, gizzards]
        methods: [boil_simmer, braise]
        answers: {dry_state: liquid_low}
        response: כאן כותבים טיפול שנבדק למצב המסוים הזה.
```

Selectors within a variant are ANDed; values within a selector list are ORed.
Supported selectors are `dish_terms` (ingredient/title phrase match, including
negation handling), `ingredient_ids` (graph IDs), `families`, `methods` (canonical
IDs or recognized labels), `stages` (`not_started`, `cooking`, `finishing`, from
an explicit progress choice), and `answers`. An unknown stage is not guessed.
Answers to diagnostic questions are scoped to that problem occurrence, rather
than reused when a problem is reported again. Updating dish details clears pending
diagnostics so they cannot be applied to a different dish.

The engine asks unanswered diagnostic questions needed by contextual candidates.
The **first matching variant in source order wins**, so place specific variants
before broad ones. Optional `response` is a fallback only after no variant matches;
omit it where a generic correction would be inappropriate. A missing rule records
the dish, ingredients, method, reported stage, diagnostic answers and description
in `missing_problem_rules`, and the UI displays an explicit gap notification.
`problem_rule_match` records the chosen variant and optional source URLs.
Fire handling stays outside editable rules and pauses the workflow.

The default dry/tough rules distinguish a pot running out of liquid, collagen-rich
cuts still tough in moist cooking, and cooked protein reported dry when eaten.
They do not recommend more cooking for every tough cut. Unknown situations and
unsupported dish/method combinations remain gaps requiring an added rule.
The collagen guidance draws on [Iowa State University Extension](https://blogs.extension.iastate.edu/answerline/tag/less-tender-cuts/).
The cooked-turkey moisture/reheating reference is [USDA FSIS](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/poultry/lets-talk-turkey-roasting).
Neither source verifies every default response for every possible dish.

Focused checks: `tests/test_decision_table.py`, `tests/test_problem_rules.py`,
`tests/test_contextual_problems.py`, `scripts/check_contextual_choices_browser.py`.
