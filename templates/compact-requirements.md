# [Capability ID] — [Action-based title]

Status: Draft  
Owner: To complete  
Last updated: To complete  
Product acceptance: Not accepted
Accepted by: To record
Accepted on: To record
Accepted scope: To establish
Acceptance evidence: To record
Material blockers: To establish

Use for a simple change; there is no page limit. Split into linked records when meaningful boundaries, decision history or delivery needs justify it. Preserve IDs and update references. All repository authority and readiness rules apply.

## Purpose and scope
Outcome, included/excluded behaviour, actor, trigger, eligibility and dependencies: To establish.
Problem evidence / source (or labelled hypothesis): To establish.
Success signal / checking method (or unknown): To establish.

## Current behaviour and evidence
Distinguish implementation, tests, intent and inference. Define evidence IDs when findings are available.

| ID | Finding / type | Source / commit / path | Conflict / gap |
| --- | --- | --- | --- |

## Required behaviour and business rules
Only confirmed new business behaviour belongs here.

| ID | Requirement or rule | Decision / shared rule |
| --- | --- | --- |

## Exceptions
Condition → response and observable state effect: To establish.

## Acceptance examples
| ID | FR/BR | Starting state and input | Action | Expected result | Review/checking method |
| --- | --- | --- | --- | --- | --- |

Where domain calculations, financial figures or effective-dated rules are in scope (standards/domain-calculations-module.md), independently check a complete numerical scenario and relevant boundaries/exceptions. Record calculation conventions and expected amounts. The implementation under test alone is not an independent check. If not applicable, explain briefly.

## Decisions and open questions
| ID | Status | Decision/question and rationale | Confirmer/date | Affected IDs |
| --- | --- | --- | --- | --- |

Use `D` IDs for decisions and `Q` IDs for questions. Preserve superseded decisions and link replacements. Recommendations and working assumptions remain visibly unconfirmed.

For material `Q` packets, use a separate table or linked subsection:

| ID | Decision needed / why owner | Classification / evidence checked | Options and recommendation / tradeoff | Scenario / consequences | Owner / priority | Status | Blocks |
| --- | --- | --- | --- | --- | --- | --- | --- |

Investigate before asking. Use explicit affected IDs, `All` or `None` in `Blocks`. Declare each `Q` only once. Reconcile related choices through one complete scenario before continuing the interview.

## Readiness and acceptance
The header owns current acceptance and material-blocker metadata. Reference outstanding `Q` IDs and readiness evidence here; do not maintain a second acceptance statement.

## Checkpoint
Workflow phase: Preparation
Progress, evidence gaps, exact next step and files changed: To complete.
Last decision group / complete scenario reconciled: Not yet checked.
Measurement record / current session ID / capture gaps: To record under measurements/<capability>.json using measurements/README.md. Keep effort and unsourced human judgments unknown; link rather than duplicate observation values.

## Implementation
Complete before handoff; no separate empty file is required.
Target: <org>/<target-platform-repo>.
Handoff status: Not prepared
Requirements baseline commit SHA: Not pinned
Pinned requirements link: To record
Pinned decisions link: To record
Platform evidence commit SHA: To establish
Included IDs: To establish
Exclusions, dependencies and ADR conflicts: To establish.
Delivery state: Not started.
Tickets/PR/implementation commit, coverage, commands/results/environment/limitations and delivered-scope acceptance: Not established.
Pin the earlier accepted requirements commit in a later commit. Follow standards/delivery-workflow.md; requirements acceptance does not authorise implementation, merge or deployment.
Set Handoff status to Prepared only after scoped acceptance and pinning. Follow standards/validation.md for field conventions.
