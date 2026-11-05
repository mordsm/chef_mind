# Dish recognition and structured reporting

At `start_custom` the server makes at most one recognition request. Its validated
classification is stored in `JourneyState.dish_identity`; saving intake details,
reporting actions and resuming a journey do not request recognition again.

Configure `CHEF_DISH_MODEL_PROVIDER=local` and
`CHEF_DISH_LOCAL_MODEL=phi4-mini:latest` to use the installed Ollama service on
127.0.0.1:11434. The local path sends no data to OpenAI. `disabled` uses explicit
rules only. `openai` uses the existing server-side API key, model and TLS settings.
Classification is rate limited, has no automatic retry or second-provider fallback,
and cannot generate recipes, timings, measurements or safety approvals. A timeout
or invalid response falls back to explicit rules and user choices.

Explicit user methods and method words in a dish title override model inference.
Method policy still validates choices. Grilled chicken resolves to grilling;
wet-cooking goals and unrelated preparation paths are omitted from its choices.

The single action reporter has thirteen actions, with an explicit complete catalog.
`actions.json` defines their parameters and timers. Added actions preserve version-1
records and the original three action definitions. Notes are never interpreted.
The remaining free-text form is for questions only, not duplicate action entry.
