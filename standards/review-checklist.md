# Proportional review checklist

Use only applicable checks. A short feature does not need a paragraph for every item.

## Core functional completeness (all capabilities)
- Outcome, actor, trigger and scope are explicit.
- Problem evidence and success signal are recorded proportionately; hypotheses and unmeasured targets are labelled.
- Applicable decisions were reused and accessible evidence investigated before asking the owner. Each material question explains why an owner is needed, options, recommendation, scenario, priority and blocked scope (`Blocks`).
- Interacting decisions were reconciled through a complete scenario during discovery, not only at the end.
- Eligibility, permissions, roles and approval boundaries are defined.
- Mandatory inputs, validation rules, limits and invalid combinations are specified.
- State transitions, lifecycle preconditions and postconditions are explicit.
- Configuration scope, defaults and applicability to existing records/accounts/users are resolved where relevant.
- Failure handling, duplicate submission (idempotency), cancellation, correction and rollback/reversal behaviour are addressed or explicitly excluded with dependencies.
- Outputs, notifications, audit events and downstream observable effects are defined where applicable.

## Evidence, traceability and readiness
- Evidence has repository/source and commit/version references; conflicts and access gaps remain visible.
- Confirmed decisions support normative rules. No recommendation or working assumption has become a rule by accident.
- Examples cover relevant normal, boundary and failure cases without duplicating rules.
- IDs and cross-references (`FR`, `BR`, `EX`, `D`, `Q`, `E`) are correct. Two readers can derive the same expected outcome.
- Readiness and acceptance are explicit; unresolved material questions block readiness for their scope.
- Structural checks, behaviour review, language review and executed application tests are reported separately. Passing structure does not certify approval or business correctness.
- Record structure fits the change; no empty files are required solely by a template. Each substantive fact has an authoritative location.

## Domain-specific module check
- If the capability involves calculations, pricing, balances, schedules, accounting, or effective-dated vs. processing-dated events, also apply [standards/domain-calculations-module.md](domain-calculations-module.md).
