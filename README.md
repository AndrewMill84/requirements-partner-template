# Product Requirements Partner — Reference & Starter Repository

This repository is a clean, portable setup for an AI **Requirements Analysis Partner**. A product manager and an AI agent use this workspace to discover, reconcile and specify concise, confirmed functional behaviour—grounded in real system data sources—before an implementation agent modifies target application repositories.

It also serves as a **reference architecture** that an existing work instance can inspect to audit its own instruction files, state gates, data-source sync workflow and validation scripts. See the [Reference & Upgrade Guide](docs/reference-upgrade-guide.md) to compare an existing setup against this repository.

## Two workspaces, one delivery flow

| Workspace | Responsibility |
| --- | --- |
| **Requirements repository (this workspace)** | Data-source evidence synthesis, capability discovery, product decisions, functional requirements, acceptance examples and pinned handoff references |
| **Target implementation repository / sources** | Application code, architecture decision records (ADRs), schemas, domain documentation, implementation tickets, tests and delivery evidence |

Sync data sources → describe outcome → investigate system evidence → resolve decisions → reconcile examples → owner accepts scope → pin requirements commit → implement and verify in target repo → record results here.

A committed draft is not approval. Product acceptance and implementation verification are separate.

The agent first [prepares the evidence and decision packets](standards/discovery-workflow.md) independently using connected data sources. It reuses applicable decisions, asks only about material business choices requiring an owner, and reconciles their consequences throughout discovery. The product manager supplies intent, resolves policy and accepts the resulting scope.

## Start here
1. **Configure & sync data sources:** Open [project-context.md](project-context.md) and list your product owner, target code repositories, documentation sources and issue trackers. Run the **Bootstrap & sync data sources** prompt in [prompts/session-prompts.md](prompts/session-prompts.md) (following [standards/data-source-sync.md](standards/data-source-sync.md)) so the agent inspects your sources and populates system orientation and [standards/glossary.md](standards/glossary.md).
2. **Read core instructions:** Ensure your agent loads [AGENTS.md](AGENTS.md), [project-context.md](project-context.md) and [SETUP.md](SETUP.md).
3. **Create a capability:** Choose the [compact template](templates/compact-requirements.md) for simple changes or copy [templates/capability/](templates/capability/) for capabilities that benefit from separate records. Store either under `capabilities/<slug>/` and add it to the [capability index](capabilities/README.md).
4. **Discover and reconcile:** Use [session prompts](prompts/session-prompts.md) to discover or resume requirements. Enable [standards/domain-calculations-module.md](standards/domain-calculations-module.md) when working on calculation-heavy, financial or effective-dated rules.
5. **Hand off approved scope:** Follow [the delivery workflow](standards/delivery-workflow.md) when handing approved work to an implementation agent.

## Upgrading an existing work repository
If you already run a requirements partner repository at work and want your work agent to evaluate what to adopt from this reference setup:
- Point your work agent to [docs/reference-upgrade-guide.md](docs/reference-upgrade-guide.md) and use the **Audit and upgrade an existing requirements repo** prompt in [prompts/session-prompts.md](prompts/session-prompts.md#audit-and-upgrade-an-existing-requirements-repo).

## Records
There is no page limit. Scale detail and structure to the change; never remove necessary behaviour to shorten a specification.

Each capability records requirements, decisions and a checkpoint as sections or separate files. Add the implementation handoff before delivery. The handoff links a fixed specification version to target implementation tickets, PRs and test evidence. Keep functional rules here; reference existing target specifications rather than copying them into competing documents.

## Record responsibilities

Scale the record structure to the change. A simple change may contain requirements, decisions and a checkpoint in one file. Use separate linked records when they improve clarity, preserve substantial decision history or support implementation handoff. Do not create empty documents merely to satisfy a template. Preserve stable IDs and update links when splitting records.

| Record or section | Authoritative content |
| --- | --- |
| Requirements | Current required behaviour, scope, exceptions and acceptance examples |
| Decisions | Choices, rationale, unresolved questions and superseded alternatives |
| Checkpoint | Current progress, workflow phase and the exact next step |
| Implementation | Accepted baseline, delivery references and verification coverage |
| Investigation/review | Source evidence, findings and discrepancies |

Maintain each substantive fact in one authoritative location. Elsewhere, use a brief orientation summary and a link. When a confirmed decision changes, reconcile affected requirements and examples. Requirements express the selected behaviour; decisions explain its authority and rationale.

The product manager (or named domain owner) owns new business decisions. Existing target ADRs and domain vocabulary remain applicable unless an explicit change is agreed and reconciled. All files under `examples/` and `evals/` remain fictional and unapproved.

Writing uses an adapted ASD-STE100-based profile ([standards/writing-profile.md](standards/writing-profile.md)); full compliance is not claimed. No application runtime or external AI service is bundled.

## Offline checks and workflow evaluation

With Python 3.11+, run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_requirements.py
```

[Structural validation](standards/validation.md) checks declared IDs, table references, local navigation, readiness and prepared handoff metadata. GitHub Actions runs these checks on PRs and configured branches. It does not establish business correctness or authentic approval.

Use the [agent evaluation cases](evals/README.md) when changing prompts or instructions. Dataset integrity tests are automated; responding to and grading the cases is a separate evaluation.

## Record real workflow outcomes

[Measurement records](measurements/README.md) capture prospective session effort, questions, findings and actual handoff feedback. Agents maintain them at existing checkpoints; unknown values and agent judgments stay visibly separate from sourced human estimates/reviews.

Run `python3 scripts/measure_workflow.py --check` to validate records, `python3 scripts/measure_workflow.py` for a readable report, or add `--json` for analysis. Reports show coverage and workflow versions; they do not automatically conclude that productivity improved.
