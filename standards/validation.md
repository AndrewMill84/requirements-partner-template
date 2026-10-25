# Structural validation

Run from the repository root with Python 3.11 or later:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_requirements.py
```

Both commands run offline with the standard library. CI uses the same commands. Exit 1 means structural findings; exit 0 means the supported checks found none. It does not mean requirements are approved, domain-correct or implemented.

## Active records and IDs

Each folder directly under `capabilities/` has `requirements.md` as its entry point. Use a compact file or linked Markdown records within that folder. Templates and fictional evaluation inputs are not active capabilities.

Declare `FR`, `BR`, `EX`, `D`, `Q` and `E` identifiers in a Markdown table whose first column is `ID`. The first cell contains one complete identifier, such as `FR-001`. IDs are unique within a capability. Retain superseded decisions. Tables with a different first-column name, such as `FR / BR` in a coverage table, reference IDs rather than declare them.

References in capability tables are checked against those declarations. Full ranges such as `FR-001–FR-004` include the intervening IDs. Write every ID in abbreviated lists explicitly: `FR-001, FR-002`. Cross-capability references use `other-capability:FR-001`. The `other-capability` part is the folder name. Bare references use the current capability's namespace.

Narrative mentions outside tables and external platform rule/invariant identifiers are outside this ID check. An ID reference is not evidence that a decision is confirmed or that an example establishes the right outcome.

## Readiness

Put these fields before the first second-level heading in `requirements.md`:

```text
Status: Draft
Owner: To complete
Product acceptance: Not accepted
Accepted by: To record
Accepted on: To record
Accepted scope: To establish
Acceptance evidence: To record
Material blockers: To establish
```

`Draft` and `In review` records may contain incomplete work. `Superseded` is also a valid status. Before declaring `Ready for engineering`, record `Product acceptance: Accepted`, the actual accepter, a real ISO date (`YYYY-MM-DD`), explicit accepted `FR`/`BR`/`EX` IDs, evidence of the confirmation and `Material blockers: None`. Accepted scope contains only `FR`/`BR`/`EX` IDs and includes at least one obligation (`FR` or `BR`) and one `EX`. A `BR`-only change is permitted when its examples establish the selected behaviour. Scope may be narrower than the whole capability.

Open-question tables should include `Status` and `Blocks` columns. Use `Open`, `Proposed` or `Unresolved` for outstanding rows; `Blocks` contains explicit affected IDs, `All`, or `None`. `Deferred` rows also remain unresolved for their declared scope. An outstanding/deferred row blocking accepted IDs fails readiness. Retain deferred questions with their separate scope. This check cannot find hidden blockers or understand every natural-language classification; the behaviour reviewer checks those.

## Prepared handoffs

Use `implementation.md`, or fields in the compact file when no separate handoff exists:

```text
Handoff status: Not prepared
Requirements baseline commit SHA: Not pinned
Platform evidence commit SHA: To record
Pinned requirements link: To record
Pinned decisions link: To record
Included IDs: To establish
```

Set `Handoff status: Prepared` only after the accepted baseline is committed. Both commits must be full 40-character SHAs. Each pinned field contains one bare URL or one inline Markdown link whose actual destination uses `https://github.com/<owner>/<repo>/blob/<requirements-baseline-sha>/<path>`; compact requirements and decisions may share one URL. Labels do not establish the destination. Included IDs must contain only `FR`/`BR`/`EX` IDs, be within accepted scope and include at least one obligation (`FR` or `BR`) and an acceptance example. Delivery states `In progress`, `Implemented`, `Verified` and `Accepted` require a prepared handoff and ready accepted requirements. `Draft`/`Blocked`/`Not started` work may remain unpinned.

The validator checks URL shape and matching SHA strings, not remote availability, Git object existence, source authenticity, calculation independence or the approved contents at that commit. Review these before handoff. A remote baseline is deliberately not fetched by CI.

## Links and limits

Checks cover inline Markdown links, local file existence and ATX heading fragments, including repeated heading suffixes. External links are not fetched. Fenced code, inline code link examples and HTML comments are ignored. This is a small convention checker, not a complete CommonMark parser: reference-style links, HTML anchors, setext headings, embedded HTML and arbitrary Markdown extensions need separate review. Use the supported forms for new repository navigation.

The agent review uses [the review checklist](review-checklist.md) to examine authority, omissions, contradictions, calculations and scenarios. The [evaluation cases](../evals/README.md) measure the requirements agent's behaviour separately. Neither structural tests nor model agreement replaces product decisions or specialist validation.
