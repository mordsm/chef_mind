# Station response contract

Both current-action guidance and the Chef response panel render the server's
`station_protocol`: six ordered blocks followed by at most one next question.
The same object provides the downloadable Obsidian note. Historical `messages`
remain conversation history; clients must render the contract as the guidance.

The implementation is deterministic and makes no new provider calls. It uses
the dish name, local ingredient registry, reported family, current step, safety
holds and source records. A missing method/station profile or disabled classifier
sets `knowledge_gap_flagged`; it does not terminate the response. Unsupported
times, temperatures and pagination are explicitly `UNKNOWN`, never invented.
Approved claim citations remain distinct from editorial family protocols.

## Sources and limits (evidence cutoff: 2026-11-04)

- Harold McGee, *On Food and Cooking*, 2nd edition (2004), chapter 4,
  printed pp. 179–242; gentle poaching pp. 215–217. Page mapping comes from
  the existing local `SRC-MCGEE-2004` and `TEC-FISH-002` source records.
  These are general fish principles, not validation of a Nile-perch recipe.
- [FDA Food Code 2022](https://www.fda.gov/media/164194/download),
  sections 3-401.11(A)(1) and 3-501.14: proposed default for intact, unstuffed
  finfish is 63°C for 15 seconds; cooling from 57°C to 21°C within two hours
  and to 5°C within six hours total. The profile requests storage below 4°C
  as an additional operating target. This does not certify a kitchen HACCP
  plan or establish local regulatory compliance. Minced, stuffed and frozen
  fish are outside this station heating protocol.
- [Lindholm-Lehto et al., whitefish depuration research](https://pmc.ncbi.nlm.nih.gov/articles/PMC6801251/):
  evidence about geosmin/2-MIB accumulation and removal in farmed whitefish;
  extrapolation to a particular Nile-perch fillet is explicitly unverified.
- [Sovann Kin, food-grade ingredients and catfish off-flavors](https://scholarsjunction.msstate.edu/td/2707/):
  primary experimental dissertation. Reductions differ between geosmin and
  MIB and between treatments; it does not establish a universal brief acid,
  salt or milk protocol for Nile perch. The UI makes no complete-removal claim.
- [Domaine Amirault, Anjou Blanc technical sheet](https://www.domaineamirault.com/wp-content/uploads/2023/08/Fiche-TecH-FDFAnjou-blanc-EN-1.pdf):
  identifies dry Chenin Blanc from Anjou and a cooked-fish pairing.
  The station pairing is an editorial suggestion, not an experimentally
  established optimum. A nonalcoholic option is shown.
- [IUCN species record](https://iucngisd.org/gisd/speciesname/Lates%2Bniloticus):
  identifies Nile perch (*Lates niloticus*) as a freshwater fish.

The ckbk excerpt was discoverable in search but full retrieval returned 403;
the book pagination relies on the previously indexed local source records.
No comprehensive literature review, kitchen experiment, species-specific
marinade study or sensory panel was performed. Remaining work includes
validated marinade concentration/duration, thickness-specific heating data,
and professional review of kitchen-specific hazard controls.

## Safety approval

`backend/app/data/station_profiles.yaml` stores the approval state. While it is
`PENDING_OWNER_APPROVAL`, fish preparation remains cold and no heating target is
authorized by this contract. Numeric approved-policy tests use an isolated
configuration fixture; they must not be represented as owner approval.
Ambient sauce temperature and core temperature are always distinguished;
rest/carryover is never used to compensate for an unmet safety endpoint.
Allergy conflicts, method warnings and safety holds override cooking advice.

## Verification

`tests/test_station_protocol.py` covers missing method and station profiles,
disabled classification, both APIs, note frontmatter, safety holds, fish allergy
without inventory, out-of-scope fish and preserving the user's chosen method.
`scripts/check_station_protocol_browser.py` exercises the named dish, fish-family
selection, asking the Chef, six visible blocks and note downloads at 1440/390px.
It uses an in-memory database and disables both model features.
