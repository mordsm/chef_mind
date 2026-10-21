# Common problems and response rules

The single **יש בעיה** button opens common problems. Selecting a problem calls
the local rules table without a model. Initial rules cover scorching, sticking,
overly thick/thin sauce and excessive salt. Dryness, toughness and other problems
are shown even when their response rule is missing. The interface explicitly
reports a missing rule and stores its ID, method and description in the journey's
`missing_problem_rules` backlog; it does not invent treatment instructions.

Open **Knowledge → כללי טיפול בבעיות — הוספה ועריכה**. Guest users can read the
defaults. A connected reviewer can edit YAML, check the review checkbox and
choose **שמור ואשר כללי תגובה** to activate a private revision for that account.
Changes take effect on the next authenticated cooking command. Guest cooking
continues using the packaged defaults in `backend/app/data/problem_rules.yaml`.

Example entry under the existing `rules` mapping:

```yaml
rules:
  too_dry:
    response: "Your reviewed response and follow-up question here."
    methods: ["מחבת"]
```

An omitted/empty `methods` list makes a rule available for every method. A
nonmatching method produces the same explicit missing-rule alert. The editor
lists valid problem IDs. Rules are plain text, not executable expressions.
Fire is handled by the fixed safety policy and cannot be overridden here.

Authenticated GET/PUT `/v1/coach/problem-rules` returns/saves YAML with optimistic
`expected_revision`; PUT requires reviewer permission and `reviewed: true`.
Public GET `/v1/coach/problem-rules/template` returns only the packaged defaults.
All revisions use the existing versioned configuration table and logical backup.
