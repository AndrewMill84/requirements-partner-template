# Prepare, decide, reconcile and specify

## Independent preparation

Start from a brief, voice-note transcript, issue or customer request. Establish the problem, affected actor, intended outcome and known constraints. Record the source of the problem and a success signal proportionate to the change; if these are hypotheses, label them. Do not invent customer evidence, targets or priorities.

Investigate accessible decisions, rules, system documents, code and tests at a recorded version before detailed questions. Check scope, applicability and conflicting sources. Prepare:

- The problem, outcome, scope and success signal.
- Current-to-target behaviour and affected interfaces or capabilities.
- Applicable confirmed decisions and source constraints.
- Contradictions, evidence gaps and proposed scenarios.
- The small set of material business choices still requiring an owner.

Use existing requirements, decisions and investigation sections; add a separate record only when it improves navigation. Confirmed parts can be drafted immediately. Place new proposed behaviour in the question/proposal section until confirmed. If missing intent prevents useful preparation, ask the minimum scope question first and continue unaffected investigation.

On resume, read the checkpoint and recheck affected sources. Do not repeat a completed investigation or reopen applicable decisions merely to fill a template.

## Classify before asking

| Classification | Agent action | Escalation condition |
| --- | --- | --- |
| Applicable confirmed authority | Apply and cite its decision/rule and scope. | A conflict, changed applicability or requested replacement. |
| Current behaviour / constraint | Inspect source and distinguish implementation, tests and intent. | The intended outcome is uncertain or conflicts with authority. |
| Bounded engineering choice | Leave the mechanism to implementation under target repository conventions. | It changes observable product behaviour, controls or an agreed constraint. |
| Missing evidence | Investigate available sources; record unavailable access. | An inaccessible fact materially blocks the next decision. |
| New or conflicting business policy | Prepare a decision packet for the authorised owner. | The owner selects the behaviour; no silent default. |
| Future enhancement | Record as deferred with its dependency and scope. | It becomes necessary for the selected release outcome. |

Existing code is evidence of current behaviour, not automatic authority for desired behaviour. Verify that inherited rules actually apply; a familiar name is insufficient. A consequence logically derived from agreed rules needs an explanation and example, not a fresh policy choice. If deriving the example requires selecting another rule, raise that choice.

## Decision packet

Extend the existing Q row or linked section with: decision needed; classification; evidence checked and why it is insufficient; options; recommendation/tradeoff; scenario/consequences; owner; priority; status; blocked IDs. Use explicit IDs or `All` in the `Blocks` column for automated scoped readiness checks. `None` means the question does not block current acceptance.

Group related choices, normally one to three at a time. Prefer a concrete scenario that reveals the difference between options over a generic questionnaire. Where numerical or date-sensitive rules apply, mark actual versus projected figures, dates, assumptions and checking method ([domain-calculations-module.md](domain-calculations-module.md)). Do not calculate through a missing policy as if the result were confirmed.

An unresolved decision blocks its affected scope. Independent discovery may continue. An implementation slice may proceed only if separately accepted, authorised and demonstrably independent; do not assume that superficially separate rules can be safely split.

## Reconcile during discovery

After a related group of decisions:

1. Check interactions with earlier decisions, exceptions and system constraints.
2. Walk one complete scenario from starting state to observable outcome.
3. Identify any state transition, calculation, permission or lifecycle rule needed to finish it.
4. Update affected requirements/examples and retire obsolete proposals.
5. Explain what is settled, what still blocks the scope and the next useful action.

Where calculations or effective-dated rules are in scope, start concrete fixtures early ([domain-calculations-module.md](domain-calculations-module.md)). Separate business policy decisions from missing implementation. Use independently checked expected results before readiness; a prototype or the same implementation's output alone is not independent validation.

## Review, readiness and handoff

Review behaviour using [the checklist](review-checklist.md) (and [domain-calculations-module.md](domain-calculations-module.md) when applicable), then language using [the writing profile](writing-profile.md). A behaviour finding identifies affected IDs, source evidence, consequence, recommended correction and whether a human decision is required. Fresh agent review provides scrutiny, not proof of correctness.

Apply [structural validation](validation.md). Record explicit scoped acceptance only when actually given. Follow [delivery workflow](delivery-workflow.md) to pin the accepted baseline and prepare implementation work. A proposed scope split or passing structural check does not authorise implementation.

Keep workflow phase separate from requirements status and delivery state. Suggested checkpoint phases: `Preparation`, `Decisions`, `Reconciliation`, `Behaviour review`, `Handoff`. A completed preparation phase can still leave requirements `Draft`.

## Improve the process

Track avoidable questions, unsupported assumptions caught, missed material decisions, product-manager effort and rework caused by misunderstood requirements. Review small samples of actual sessions; do not invent quantitative improvement claims. Turn observed failures into [evaluation cases](../evals/README.md). Evaluate instruction changes against those cases before adding orchestration.

Use the [measurement records and protocol](../measurements/README.md) at substantive checkpoints and after actual handoff feedback. The agent records observations; human time and human judgments require attributable sources or remain `unknown`. Reports distinguish incomplete capture, agent assessment and human review. Tracking is prospective unless historical evidence actually exists.
