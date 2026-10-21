# Provider controls and diagnostics

Seven implementation steps before checks: configurable bounds, thread-safe request reservation, safe error classification, decision/audit integration and stale-state preflight, reviewer diagnostics, regression cases, and operating/configuration documentation.

Add optional values to the ignored project `.env`, then restart Chef Core:
```dotenv
CHEF_MODEL_TIMEOUT_SECONDS=20
CHEF_MODEL_MAX_OUTPUT_TOKENS=400
CHEF_MODEL_CALLS_PER_MINUTE=30
CHEF_MODEL_USER_CALLS_PER_MINUTE=10
```
Server enablement and per-request `allow_external_model=true` remain necessary. Zero automatic SDK retries remain configured. Timeout range is 1–60 seconds, output limit 100–2000 tokens, and request limits 1–1200 per rolling minute. These controls bound request volume and requested output, **not a guaranteed monetary spend**. Provider billing/credits are separate. Rate limits are process-local; use one API worker or add shared coordination before scaling to multiple workers. Failed attempts consume the reserved minute slot to avoid error loops. Counters and reservations reset on process restart.

Reviewer-only GET `/v1/operations/provider` reports safe configuration, whether a key is configured, and counters for the authenticated owner. It never calls OpenAI or returns API keys, raw errors, user text or other owners' counters. A configured key does not prove valid authentication, model access or available credits. Readiness remains database readiness, not a paid provider probe.

Chef decisions expose `provider_status` and nullable `provider_latency_ms`; the same fields are stored in the cooking record and `CHEF_DECISION` audit event. Duration includes the model adapter/TLS work and is not a token-usage or billing estimate. Existing engine and policy flags remain available.

| Status | Meaning / operator action |
| --- | --- |
| selected | Structured source selected; local policies still decide the final action |
| disabled / not_requested | Server disabled the model or request did not opt in |
| no_candidates | No approved retrieval candidates; no paid model call |
| policy_blocked | Local safety/dietary clarification or block prevented a model call |
| local_rate_limited | Local request budget reached; wait for the rolling window |
| quota_exhausted | Provider reported exhausted credits/quota; check API billing |
| authentication_or_access | Key or access permission issue; check project configuration |
| provider_rate_limited | Provider request limit; wait/check provider limits |
| timeout / connection_error | Provider call did not complete; check connectivity |
| invalid_output | Structured provider response failed validation |
| provider_error | Other provider HTTP error; investigate privately |

On provider failure or a local limit, extractive decisions still pass the same policy checks and expose fallback plus classified flags. Preflight rejects known-stale state and applies stored allergies before an external call. The final transaction locks and refreshes the state again because another request may have changed it during inference. A conflict occurring during a paid call can still incur usage; preflight cannot eliminate all concurrent spending. Attempt counters include calls even if a later state conflict prevents saving a decision; durable decision audits only exist for committed decisions.
