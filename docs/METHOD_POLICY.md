# Recommended cooking methods

The shared defaults live in `backend/app/data/method_policy.yaml`. The first
matching profile determines the allowed methods. A profile can select ingredient
IDs, title/ingredient terms and/or a dish family; all provided selectors must
match. Put specific dishes before family defaults. An unmatched dish has no
approved methods until a profile is added.

`allowed` lists method IDs. `reason` explains exclusions generally;
`blocked_reasons` can explain an individual method. Default gizzard preparation
allows `braise` and `boil_simmer`, excluding oven roasting with an explanation.
These are editable preparation preferences, not a guarantee of cooking safety.
Independent temperature/process restrictions still apply.

In the console, open **Knowledge → שיטות הכנה מומלצות — קונפיגורציה לפי מנה**.
Guests can view defaults. A signed-in reviewer can edit, review and activate a
version for their account. Guest cooking continues using the file defaults.
The editor lists available method IDs. Saved revisions are backed up with the
other configuration records; no new migration is needed.

The method dropdown shows only allowed methods and a separate explanation of
the excluded methods. The server enforces the same policy on initial plans,
plan updates, method-answer choices and adopted graph paths. A method mentioned
in a dish title is checked as well. Older plans with an excluded method retain
their reports and show a warning, so users can report a problem before editing
the plan to a recommended method.

Public GET `/v1/coach/method-policy/template` and POST
`/v1/coach/method-policy/options` expose defaults/recommendations. Authenticated
GET/PUT `/v1/coach/method-policy` and POST
`/v1/coach/method-policy/my-options` use the caller's configuration. PUT requires
`expected_revision`, `yaml_text` and `reviewed: true` with reviewer permission.
