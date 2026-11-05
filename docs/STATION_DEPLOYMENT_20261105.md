# Station protocol deployment — 2026-11-05

Deployed to https://chef-mind-gateway.chef-mind.workers.dev/ by restarting
only the verified Chef backend on loopback port 8801. The on-demand gateway,
public address and PostgreSQL data were preserved. No database migration was needed.

Owner approval recorded in `backend/app/data/station_profiles.yaml`: intact,
unstuffed finfish core 63°C for at least 15 seconds. The station specifies
70–80°C poaching liquid, no safety rest or reliance on carryover, staged cooling
and storage below 4°C. This approval does not certify kitchen-specific HACCP.

Fixed kitchen view rendering when a station-only decision omits `citations`.
Extended `scripts/check_station_protocol_browser.py` with `--url` for isolated
guest acceptance against a running deployment, without saving server journeys.

Verification:

- 63 focused regression tests passed across station protocol, coach, consultant,
  method policy and kitchen flow.
- Live public browser acceptance passed at widths 1440 and 390: Nile Perch,
  fish family, question to chef, six blocks on both guidance surfaces,
  63°C / 15 seconds, geosmin / 2-MIB, Chenin Blanc / Anjou,
  wikilinks, culinary tags, McGee chapter/pages, and Obsidian download.
- The live recognition status was `unavailable`; the complete local protocol
  remained available and flagged the gap.
- Separate offline browser acceptance passed at both widths with recognition
  explicitly `disabled` and the real approved configuration.
- Automated tests cover missing method/station profiles, API response surfaces,
  persistence and safety overrides. Approval fixtures are not the sole proof:
  browser checks exercised the actual approved YAML configuration.

Remaining content uncertainties are explicit: species-specific heating duration
depends on cut/thickness; pretreatment concentration/duration and complete 2-MIB
breakdown are unverified. These are flagged knowledge gaps, not fabricated values.

## Plain-language interface follow-up

Removed the repeated full protocol after saving dish details; a short save status
now points to the existing guidance. Scientific background and links/tags use
closed, keyboard-accessible details elements. Practical instructions remain open.
Nile Perch preparation no longer suggests an unspecified acid/milk pretreatment.
The knowledge-gap section now explains in Hebrew that the book is already in the
knowledge base while cut-specific timing and pretreatment amounts are missing.
Internal marker and book reference remain available under a separate explanation;
raw provenance IDs remain in structured data rather than the displayed prose.

45 focused tests passed, followed by 18 station tests after the final wording edit.
Browser acceptance includes assertions for collapsed background, accessible
expansion and absence of the duplicate save panel at desktop/mobile widths.

## Practical cooking explanations and linked reading

Clarified liquid temperature versus burner setting, center temperature versus
total cooking duration, the start of the 15-second hold, plain-language texture
checks, residual heat, and prompt cooling. Flavor suggestions now describe a
small lemon tasting comparison, optional toasted breadcrumbs, and beverages
served alongside the dish. Unverified acid/milk treatments remain omitted.
The expandable background explains 2-MIB and HACCP without implying a home
treatment or kitchen certification.

Added visible reading links to the broad McGee book, its focused poaching
section, and the free FDA consumer seafood guide. Coverage and access limits
are explicit. Sources checked on 2026-11-05:

- https://www.simonandschuster.com/books/On-Food-and-Cooking/Harold-McGee/9780684800011
- https://origin.ckbk.com/reference/food00011c04s001e008se003se006se002/poaching-temperatures
- https://www.fda.gov/media/164194/download (existing approved safety basis)
- https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-fresh-and-frozen-seafood-safely
- https://www.fda.gov/food/hazard-analysis-critical-control-point-haccp/haccp-principles-application-guidelines

45 focused tests and offline browser acceptance passed before deployment.
The live browser script now also checks the new practical wording, visible
source link, and absence of UNKNOWN in the fish execution instructions.

## Vault sources, time guide and shared glossary

Saved the FDA consumer guide as a source note with a Hebrew summary and a
complete readable local text snapshot (no original images/layout). Added a
Fishfiles source note recording the general 1/2/3 cm fillet time table and
its 75–85°C conditions; the station explicitly distinguishes these estimates
from its 70–80°C liquid range and retains thermometer-based completion.
Both source IDs are carried into the station export. Neither source note is
silently activated as an approved claim in the decision index.

Added a shared glossary with 21 terms, colored/bold inline buttons, accessible
definition dialog, Escape/focus restoration, and a full dictionary button.
An export script generates the same definitions in Obsidian; Dashboard links
make the new notes easy to find. Plain-language instructions now directly say
that this preparation needs no soaking and give everyday seasoning steps.

50 focused tests passed. Offline browser acceptance passed at both widths,
including glossary opening, closing, focus restoration, full dictionary,
time estimates, no-soaking instruction and seasoning text. The first browser
run exposed the full-dictionary button in a hidden footer; it was moved to the
visible header and the complete check then passed.
