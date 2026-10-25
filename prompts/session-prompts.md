# Session prompts

## Bootstrap & sync data sources (run once after setup or when adding sources)
Read [AGENTS.md](../AGENTS.md), [project-context.md](../project-context.md) and [standards/data-source-sync.md](../standards/data-source-sync.md). Inspect the connected data sources configured in `project-context.md` at their current commits or versions. Populate the `Last synced commit / version / date` and `Access status` columns, complete the `System orientation` table with exact paths and conventions, and populate [standards/glossary.md](../standards/glossary.md) with core domain terms, states and existing rule/invariant identifiers. Keep `Confirmed decision`, `Documented intent` and `Current behaviour` distinct, and flag any conflicts between documentation and code. Record any inaccessible sources honestly without inventing findings.

## Audit and upgrade an existing requirements repo
Read our current repository's `AGENTS.md`, `project-context.md`, `standards/`, `templates/` and `scripts/`, and compare them against the reference repository at `[path or URL to requirements-partner-template]`, including its [docs/reference-upgrade-guide.md](../docs/reference-upgrade-guide.md). Do not overwrite our domain context, active capabilities or confirmed decisions. Produce a structured gap analysis covering: (1) `AGENTS.md` scannability and the state-and-readiness gate table, (2) data-source sync and glossary authority separation, (3) independent preparation, the 6-way question classification matrix and `Blocks`-scoped decision packets, (4) early scenario reconciliation and domain calculation checks, and (5) offline structural validation, immutable handoff pinning and prospective workflow measurement. Recommend prioritized, non-breaking upgrades and wait for my confirmation before editing files.

## First session (new capability)
Read [AGENTS.md](../AGENTS.md), [project-context.md](../project-context.md) and [standards/discovery-workflow.md](../standards/discovery-workflow.md) (plus [standards/domain-calculations-module.md](../standards/domain-calculations-module.md) if calculations or effective-dated rules apply). Help me define `[capability]`. My intended outcome is `[outcome]`. These decisions are already made: `[decisions or none]`. Choose proportionate records (compact single-file or split capability folder). Independently investigate accessible evidence from our synced data sources and prepare current-to-target behaviour, applicable decisions, proposed scenarios and material decision packets before the detailed interview. Ask early only if missing intent or scope prevents useful preparation. Label proposals and hypotheses; do not invent rules or customer evidence. Then guide me through related business choices and reconcile examples as we decide.

## Prepare independently
For `[capability]`, read the current records and investigate only material changes or evidence gaps across our connected data sources. Prepare the problem evidence, outcome/success signal, current-to-target analysis, applicable authorities, contradictions and candidate scenarios. Classify open issues using [standards/discovery-workflow.md](../standards/discovery-workflow.md). Present only the material decisions requiring an owner, with checked evidence, options, recommendation/tradeoff, consequences and blocked IDs (`Blocks`). Save the preparation in existing records. Do not select new business policy or start target platform implementation.

## Resume
Read [AGENTS.md](../AGENTS.md) and resume `[capability]` from its requirements, decisions and checkpoint records (files or sections). Briefly state agreed scope, workflow phase and next material decision. Reuse saved preparation and investigate changed evidence or gaps since the last recorded source commit. Continue without reopening applicable confirmed decisions unless there is a conflict or I request a change.

## Reconcile a decision group
For `[capability]`, check the latest confirmed decisions against earlier choices and target system constraints. Walk one complete scenario (with concrete dates/numbers where applicable), including relevant boundaries. Show where an expected outcome needs another rule; do not fill it by assumption. Separate business choices, engineering work and missing evidence. Update affected requirements/examples and the exact next step.

## Checkpoint
Update the requirements, decisions and checkpoint for `[capability]`. Show the decisions recorded, outstanding blockers, files changed and exact next step. Keep proposals visibly unconfirmed. Do not mark the specification ready without explicit product-owner acceptance.
Follow [measurements/README.md](../measurements/README.md) to append/update the session observation, captured questions and findings from evidence actually available. Mark incomplete coverage and unknown effort honestly; do not reconstruct historical time or claim human review of your own classifications.

## Review
Review `[capability]` against [standards/review-checklist.md](../standards/review-checklist.md), [standards/writing-profile.md](../standards/writing-profile.md) and, when applicable, [standards/domain-calculations-module.md](../standards/domain-calculations-module.md). Report ambiguity, missing material decisions, contradictions and unsupported assumptions. Each behaviour finding names affected IDs, source evidence, consequence, proposed correction and whether an owner must decide. Run the structural validator under [standards/validation.md](../standards/validation.md) and report its result separately. Propose edits without choosing unresolved business behaviour. Distinguish behaviour review from language review and executed tests.

## Evaluate the requirements workflow
Follow [evals/README.md](../evals/README.md) to evaluate the current instructions using the cases in [evals/cases.json](../evals/cases.json). Give the responding agent the case context and task without the answer rubric. Save responses, score each rubric dimension with cited response evidence, and record human versus model review and unresolved disagreements. Report omissions, invented policy and unnecessary questions separately. Do not claim that dataset integrity tests constitute an agent evaluation or product acceptance.

## Change a decision
For `[capability]`, I want to reconsider `[decision ID]`. Show affected requirements and examples. After I confirm the replacement, mark the previous decision `Superseded` and update the affected records.

## Prepare platform handoff
Read [standards/delivery-workflow.md](../standards/delivery-workflow.md). For `[capability]`, verify explicit product-owner acceptance and remaining blockers. Prepare the implementation handoff file or section with scoped `FR`/`BR`/`EX` IDs, the accepted requirements commit, target platform evidence commit, existing behaviour/rule mappings and validation expectations. If approval or the baseline commit is missing, record that blocker. Do not start implementation or create target platform tickets unless instructed.

## Implement approved requirements (use in target implementation repository)
Read this repository's `AGENTS.md` and follow its workflow. Implement `[capability]` from `[immutable requirements repo commit URL / capability path]`. Read the pinned requirements, decisions and examples; use the implementation record as the handoff. Compare the target codebase against evidence commit `[SHA]`. Surface material ambiguities and ADR conflicts before affected implementation. Follow the target repository's ticket and architecture conventions, map requirement IDs to tests, and report exact changes, commands, results and limitations. Do not merge or deploy without authorisation.

## Review delivered behaviour
Compare `[target PR / commit]` against `[capability]` at requirements baseline `[SHA]`. Map scoped requirements and examples to implementation and actual test evidence. Record gaps in the implementation and checkpoint records. Do not infer product acceptance from passing tests.
Record actual handoff clarification feedback and downstream findings under `measurements/<capability>.json`, with baseline/scope, review source, cause and sourced rework effort. Keep unknowns and agent judgments explicit.

## Review workflow outcomes
Read [measurements/README.md](../measurements/README.md) and run `python3 scripts/measure_workflow.py`. Compare like capabilities and workflow versions, showing effort coverage, complete/partial question capture, human versus agent judgments, findings by stage/cause and handoff-review denominators. Explain missing baselines, confounders and follow-up limits. Recommend a process change only from the evidence; do not equate fewer questions, more documents or passing evals with improvement. Record the review and chosen follow-up in the relevant checkpoint; do not alter product decisions from a metric.
