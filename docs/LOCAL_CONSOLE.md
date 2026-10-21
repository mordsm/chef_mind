# Local Chef Core console

Open http://127.0.0.1:8800/ after starting Chef Core. This console belongs to the standalone `chef_mind` service; Cook Pilot is unchanged. No frontend build step or third-party assets are required. The Docker backend copy includes the static files.

Seven implementation steps before checks: responsive shell/full-screen controls, Hebrew/English interface and RTL, authenticated source catalog, pending review queue, revision/review/recovery controls, cooking form with editable inventory and citations, then tests and this guide.

## Connect

Inventory saves locally under the authenticated user ID and, after a short debounce, to the owner-scoped `/v1/inventory` endpoint. A browser without a local copy restores the server inventory. Before the first explicit inventory save, the server recovers the most recently used nonempty inventory from historical cooking records ordered by decision audit date. An explicitly saved empty inventory prevents deleted items reappearing. Local edits take precedence on the same browser. Tokens are never stored. Disconnect hides rows and allergen summaries but retains saved inventory.

Rows contain only ingredient, quantity, unit, and remove; one shared header labels the list. Classification and ingredient allergens are derived from a limited Hebrew/English catalog and retained as request metadata. Detected ingredient allergens appear together below the list, separately from the user's allergies-to-avoid profile; they are never added to the avoidance profile automatically. Unknown products do not certify absence of allergens. Suggestions never mark availability or labels verified.

The connective-tissue identification response is a short self-check without a confirmation loop. It does not authorize cooking or certify doneness. Other conditions remain explicit and can be confirmed in an expandable control. Versioned educational summaries in `culinary_basics.py` explain cooking methods and similar dishes with source links, including when no approved recipe is available. These summaries are separate from approved action citations and never supply invented times or temperatures.

Enter the **Chef Core access token** from the key of `CHEF_API_KEYS` in the local ignored `.env`. This is not `CHEF_OPENAI_API_KEY`. The console calls `/v1/session` to identify role and owner. Tokens remain in JavaScript memory for this tab and are not placed in URLs, cookies or browser storage. Reloading loses the token and current session handle. Disconnect clears rendered private data and cooking inputs. Server-side cooking records remain retained under the existing API policy.

The unauthenticated root serves only the interface shell. All private data and actions require the existing Bearer authorization. Reviewer actions remain protected on the server even if someone modifies button visibility. Cook-role catalog results contain active source metadata only, never newer pending draft content. Catalog responses are paged at 100 sources; the pending review queue and per-source history currently retain their existing unpaged contracts.

## Cook

See [Starting guidance](STARTING_GUIDANCE.md): reports and the question are optional before starting, responses receive visible focus, missing coverage exposes approved topics, and ingredients share a compact desktop row. No invented initial observations are required.

Enter a goal, current question and actual reports. Conditions should be reported only when verified: the current engine matches explicit condition text and does not silently infer it. Add ingredient names, quantities and units. Quantities accept integers or decimals and are not rounded to fixed trailing zeros. Inventory entry does not certify package labels or food safety.

Set allergies and meat/dairy separation explicitly. Existing-session dietary changes require confirmation. Each submitted request includes the inventory currently displayed, with additions/removals. The current form covers source-grounded guidance, not recipe discovery or complete recipe generation. New cooking session creates a new cooking ID; it preserves visible ingredient inputs for convenience. Disconnect clears them. The interface displays action, reason, observable success signal and attributed citations, and identifies fallback to local knowledge.

OpenAI selection is unchecked by default and requires confirmation when submitting opted-in text. Source catalog browsing, review and inventory editing do not invoke OpenAI. Approved content retains its authored language; changing interface language does not translate source material or model/engine output. No professional validation or food-safety certification is implied by the console.

## Review

Reviewer accounts can synchronize the Vault, inspect pending drafts, read source/reuse metadata and all structured units, view revision history and compare against the active revision. Every approval, rejection, retirement or rollback requires a typed reason and confirmation. Stale revision and active-pointer conflicts remain server-enforced. These controls make human review concrete; they do not automatically approve new knowledge. Only the latest pending revision can be approved/rejected. Rollback remains limited to previously approved revisions and fresh gates.

The browser renders source and error content as text, not raw HTML. Console assets use a restrictive same-origin Content Security Policy; no third-party scripts/fonts/images are loaded. API responses and shell use `Cache-Control: no-store`. Swagger at `/docs` retains its existing separate CDN-based UI and is not covered by the console CSP. Keep this development service on loopback; the console does not add production identity management or public hosting.

## Verification

The API/regression suite passed 76 tests, including PostgreSQL integration. JavaScript syntax was checked with Node. `scripts/check_console_browser.py` runs a headless Edge smoke against the running console, intercepting API calls with synthetic data so it neither reads real credentials nor activates live knowledge. It covers RTL/English switching, tab-memory login, text-escaped malicious titles, draft approval, decimal inventory, add/remove controls, local-only cooking, 1440px/390px layout widths and disconnect clearing. Install dev dependencies and have Microsoft Edge available, then run `python scripts/check_console_browser.py` from the repository root. Synthetic screenshots are written to ignored `.runtime/console-desktop.png` and `.runtime/console-mobile.png`. The smoke does not certify other browsers or physical mobile-device behavior.
