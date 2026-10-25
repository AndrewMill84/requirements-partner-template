# Reference & Upgrade Guide for Existing Requirements Partner Repositories

Use this guide when you have an existing requirements partner repository (for example, a work instance already connected to your team's repositories and domain) and want your agent to compare its setup against this reference architecture and propose targeted improvements.

---

## 1. Key structural improvements in this reference

When comparing an earlier or custom requirements partner setup against this repository, inspect these nine design pillars:

| Pillar | Reference file(s) | What makes this structure effective | Common gaps in earlier setups |
| --- | --- | --- | --- |
| **1. Scannable, lifecycle-ordered `AGENTS.md` with anti-sycophancy guardrail** | [AGENTS.md](../AGENTS.md) | Organised in exact execution order (`Role and authority` → `Start each session` → `Discover and investigate` → `Resolve decisions` → `Record responsibilities` → `Maintain the files` → `Validate and finish` → `State and readiness gates` → `Persistence` → `Writing` → `Data sources and handoff` → `Keep discovery efficient` → `Record workflow outcomes`). Explicitly balances **Prioritise accuracy over agreement** (challenge weak assumptions, contradictions and material risks with a better alternative) with **Respect decision authority** (human owns the final business decision). | Long narrative paragraphs, scattered guardrails, or deferential instructions that cause the agent to rubber-stamp flawed assumptions without pushing back. |
| **2. Explicit state-transition & readiness gate table** | [AGENTS.md#state-and-readiness-gates](../AGENTS.md#state-and-readiness-gates), [standards/validation.md](../standards/validation.md) | Separates four orthogonal dimensions: **Workflow phase** (`Preparation`, `Decisions`, `Reconciliation`, `Behaviour review`, `Handoff`), **Requirements status** (`Draft`, `In review`, `Ready for engineering`, `Superseded`), **Handoff status** (`Not prepared`, `Prepared`), and **Delivery state** (`Not started`, `In progress`, `Implemented`, `Verified`, `Accepted`, `Blocked`), with explicit entry criteria and required authority for each. | Conflating "preparation complete" or "green CI" with `Ready for engineering`, or marking handoffs ready before pinning an immutable commit SHA. |
| **3. Six-way question classification before asking** | [AGENTS.md#resolve-decisions](../AGENTS.md#resolve-decisions), [standards/discovery-workflow.md#classify-before-asking](../standards/discovery-workflow.md#classify-before-asking) | Requires the agent to classify every candidate question into `Applicable confirmed authority`, `Current behaviour / constraint`, `Bounded engineering choice`, `Missing evidence`, `New or conflicting business policy`, or `Future enhancement` *before* interviewing the product manager. | Asking the product manager engineering implementation questions, re-asking already settled decisions, or silently treating existing code bugs as product policy. |
| **4. Scoped `Blocks` column in question registers** | [standards/validation.md#readiness](../standards/validation.md#readiness), [templates/capability/decisions.md](../templates/capability/decisions.md) | Every open or deferred question (`Q-*`) declares `Blocks` (`All`, `None`, or specific `FR-*`/`BR-*`/`EX-*` IDs). Automated validation blocks `Ready for engineering` only when an unresolved or deferred question blocks an ID inside `Accepted scope`. | Either blocking an entire capability over a deferred phase-2 question, or allowing unresolved questions to silently slip into an accepted slice. |
| **5. First-class data-source sync & conflict separation** | [standards/data-source-sync.md](../standards/data-source-sync.md), [project-context.md](../project-context.md), [standards/glossary.md](../standards/glossary.md) | Defines an explicit bootstrap and per-capability sync workflow across codebases, ADRs, docs and trackers. Strictly separates `Confirmed decision`, `Documented intent` and `Current behaviour`, and logs doc-vs-code conflicts with pinned commit SHAs. | Assuming the agent knows the target system layout without a recorded orientation sync, or importing code/doc descriptions directly as confirmed product rules. |
| **6. Proportionate record scaling (compact vs. split)** | [AGENTS.md#record-responsibilities](../AGENTS.md#record-responsibilities), [templates/compact-requirements.md](../templates/compact-requirements.md), [templates/capability/](../templates/capability/) | Allows small changes to live in one `requirements.md` file while larger capabilities split into `requirements.md`, `decisions.md`, `checkpoint.md` and `implementation.md`—with identical ID and readiness validation across both layouts. | Forcing 4–5 boilerplate files for a trivial validation rule change, or cramming a 30-decision capability into an unnavigable single file. |
| **7. Early scenario reconciliation & optional calculation module** | [AGENTS.md#validate-and-finish](../AGENTS.md#validate-and-finish), [standards/domain-calculations-module.md](../standards/domain-calculations-module.md) | Requires walking one complete scenario after each decision group (not just at the end). Isolates calculation/financial/effective-date rules in a dedicated module requiring independent numerical checks (never using the implementation under test as its own oracle). | Discovering contradictions between decisions only after drafting the full spec, or using unreviewed prototype output as the expected test result. |
| **8. Two-step immutable handoff pinning** | [standards/delivery-workflow.md#2-freeze-the-handoff](../standards/delivery-workflow.md#2-freeze-the-handoff), [standards/validation.md#prepared-handoffs](../standards/validation.md#prepared-handoffs) | Commits the accepted baseline first, then records the full 40-character requirements baseline SHA, immutable blob URLs and target system evidence SHA in `implementation.md` in a subsequent commit. | Pointing implementation agents at a moving branch (`main`) or leaving handoff links unpinned. |
| **9. Coverage-aware prospective workflow measurement** | [AGENTS.md#record-workflow-outcomes](../AGENTS.md#record-workflow-outcomes), [measurements/README.md](../measurements/README.md), [scripts/measure_workflow.py](../scripts/measure_workflow.py) | Tracks session effort, question avoidability, early vs. late findings and first-handoff usability prospectively at checkpoints, keeping `unknown` effort and `agent` self-assessments strictly separate from sourced `human` reviews. | Inventing historical baselines, guessing human effort from chat timestamps, or pooling agent self-grading with human review. |

---

## 2. How to run a self-audit on your work instance

1. Make this reference repository accessible to your work agent (as a sibling checkout, an attached workspace folder, or via GitHub read access).
2. In your work repository session, run the **Audit and upgrade an existing requirements repo** prompt below (also available in [prompts/session-prompts.md](../prompts/session-prompts.md#audit-and-upgrade-an-existing-requirements-repo)).
3. Review the agent's gap report and choose which structural upgrades to apply in a dedicated branch/PR without overwriting your work repository's domain context, active capabilities or connected data sources.

### Copy-paste prompt for your work instance

```text
Read our current repository's AGENTS.md, project-context.md, standards/, templates/ and scripts/, and compare them against the reference repository at [path or URL to requirements-partner-template], including its docs/reference-upgrade-guide.md.

Do not overwrite our work domain context, active capabilities or confirmed decisions. Instead, produce a structured comparison report covering:
1. AGENTS.md structure and scannability: Which guardrails, bold lead-in conventions or state-transition gate tables from the reference AGENTS.md are missing, weaker or less clear in our current instructions?
2. Data-source sync and glossary discipline: How does our current project-context.md and glossary setup compare with standards/data-source-sync.md (pinned commits, source authority levels, separating Confirmed decision vs Documented intent vs Current behaviour)?
3. Discovery and question classification: Are we enforcing the 6-way classification matrix, 1–3 batched decision packets with explicit 'Blocks' columns, and post-decision-group scenario reconciliation?
4. Domain calculation / specialist checks: Which parts of standards/domain-calculations-module.md or standards/review-checklist.md should be enabled or adapted for our product domain?
5. Validation, handoff pinning and workflow measurement: Which offline checks (validate_requirements.py, measure_workflow.py, unit tests) or handoff metadata conventions can we adopt or tighten?

Group your recommendations into:
- High-leverage, non-breaking improvements (can be applied immediately to AGENTS.md and standards/)
- Template and validator upgrades (and whether any existing capability files would need migration)
- Optional workflow measurement or evaluation additions

Wait for my selection before editing any files.
```
