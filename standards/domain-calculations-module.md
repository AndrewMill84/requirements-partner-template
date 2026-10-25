# Optional module: Domain calculations, financial rules and effective-dated state

Activate this module when a capability involves numerical calculations, financial/billing logic, balances, schedules, quotas, accounting ledgers or effective-dated state transitions.

## 1. Additional discovery and review checks
Apply these checks alongside [standards/review-checklist.md](review-checklist.md):
- **Effective dates vs. processing/posting dates:** Specify whether rules and calculations depend on the business/effective date of an event or the timestamp when the system recorded/processed it.
- **Backdating, future dates and calendar rules:** Define how backdated inputs, future-dated schedules, time zones, cut-off times and business-day calendars behave where applicable.
- **Formulas, precision, rounding and units:** State calculation conventions, internal vs. display precision, rounding modes (e.g., `ROUND_HALF_UP`), rounding points (per step vs. at output), currencies/units and zero-floor/cap rules unambiguously.
- **State, balance and schedule effects:** Make effects on balances, accruals, quotas, schedules, aging/arrears and status explicit. Distinguish immutable historical/contractual records from derived actual positions and forward projections/forecasts.
- **Order of operations and allocation precedence:** Where multiple events occur on the same date or a single action allocates across multiple buckets/obligations, specify exact ordering and tie-breaking rules via a decision table.
- **Reversals, adjustments and replay:** Specify whether corrections mutate state in place or append compensating adjustment events and trigger effective-dated replay.

## 2. Independent calculation validation gate
Where calculations are in scope, `Ready for engineering` requires **independently checked numerical examples** (`EX-*`) sufficient to establish expected results:
- Cover at least one complete end-to-end scenario plus relevant boundary, rounding or exception cases in proportion to the change.
- Record exact starting state, dated inputs, calculation conventions, intermediate/final expected amounts and the **checking method** (e.g., reviewed manual calculation, separate spreadsheet or an independent verification script under `scripts/`).
- **No self-certifying oracles:** Expected values generated solely by the implementation under test, or by an unreviewed exploratory calculation during discovery, do not constitute independent validation.
- Distinguish exploratory calculations (used during discovery to illustrate options in a decision packet) from approved, independently checked acceptance examples.
- When deterministic verification scripts are added for complex worked examples (e.g., checking fixture JSON/tables with independent `Decimal` and `Fraction`/integer arithmetic), run them in CI alongside `python3 scripts/validate_requirements.py` and keep their scope distinct from application test execution.
