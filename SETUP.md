# Setup, data-source sync and daily use

## 1. Open the workspace and attach data sources
Clone your requirements repository and, where local code inspection is used, your target implementation repositories into a common parent folder:
```bash
git clone https://github.com/<org>/<requirements-repo>.git
git clone https://github.com/<org>/<target-platform-repo>.git
```
Open the requirements repository in your agent tool and attach the sibling implementation checkout(s), MCP servers (e.g., GitHub, Jira/Linear, Confluence/Notion), or read-only documentation exports. Confirm actual access and paths; do not assume the agent can see another folder or external service without verification.

## 2. Configure and sync your data sources
Before starting your first capability, connect the agent to your product's sources of truth:
1. Edit [project-context.md](project-context.md) to fill in the **Owner and product decision authority**, **Requirements repository**, **Target implementation repositories**, and the **Connected data sources** table (code repos, ADRs, domain docs, schemas, issue trackers).
2. Run the **Bootstrap & sync data sources** prompt from [prompts/session-prompts.md](prompts/session-prompts.md) (following [standards/data-source-sync.md](standards/data-source-sync.md)).
3. The agent will inspect accessible sources at a recorded commit/version, populate the **System orientation** table in [project-context.md](project-context.md), extract authoritative domain terms into [standards/glossary.md](standards/glossary.md) (distinguishing `Confirmed decision`, `Documented intent`, and `Current behaviour`), and explicitly log any access gaps or source conflicts.
4. Review and commit the synced context and glossary before starting feature discovery.

## 3. Load instructions
Ask the requirements agent to read [AGENTS.md](AGENTS.md), [project-context.md](project-context.md) and shared standards. [CLAUDE.md](CLAUDE.md) points Claude Code to [AGENTS.md](AGENTS.md). No paid orchestrator, custom API runner or application startup is required for this documentation workflow.

The target repository's `AGENTS.md` applies when implementing code there. Reading source code and documentation during requirements discovery does not require starting the target application runtime.

## 4. Start a capability
For a simple change, copy [templates/compact-requirements.md](templates/compact-requirements.md) to `capabilities/<slug>/requirements.md`. For larger or multi-session work, copy [templates/capability/](templates/capability/) to `capabilities/<slug>/`. Add a row to [capabilities/README.md](capabilities/README.md).

If the capability involves calculations, financial/billing rules, accounting, or effective-dated state replay, include [standards/domain-calculations-module.md](standards/domain-calculations-module.md) in the session.

## 5. Prepare the discussion independently
Use the **Prepare independently** prompt in [prompts/session-prompts.md](prompts/session-prompts.md) to obtain source evidence, current-to-target analysis, proposed scenarios and classified decision packets before detailed interview questions. Follow [standards/discovery-workflow.md](standards/discovery-workflow.md) and reuse saved preparation across sessions. Record a success signal or label it `unknown`; do not fabricate customer evidence.

## 6. Run offline checks
Python 3.11+ standard library is sufficient; no third-party packages or API keys are needed:
```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_requirements.py
python3 scripts/measure_workflow.py --check
```
See [validation conventions](standards/validation.md) before marking records `Ready for engineering` or handoffs `Prepared`. Run the [behavioural evaluations](evals/README.md) separately when updating prompts or agent instructions; a green structural check is not product acceptance.

## 7. Deliver approved scope
Review requirements and examples. Once the authorised product owner explicitly accepts the defined scope, commit and push that baseline. Record its full 40-character SHA and immutable blob URLs in `implementation.md` (or the compact specification's `Implementation` section) in a subsequent commit, then pass the handoff to the implementation agent. A commit cannot contain its own final SHA: always pin the earlier accepted content commit, not a moving branch link.

Follow [standards/delivery-workflow.md](standards/delivery-workflow.md) for tickets, traceability and verification.

## 8. Continue across sessions and track outcomes
Save decisions during discussion and checkpoint before handover. Pull latest changes before resuming elsewhere. Avoid simultaneous edits to the same capability. Resolve conflicting decisions explicitly rather than allowing Git conflict resolution to choose business behaviour.

The agent also maintains the [prospective measurement record](measurements/README.md) at substantive checkpoints. Human effort may remain `unknown`; no timer setup or per-question form is required. Use `python3 scripts/measure_workflow.py` to inspect coverage and outcomes before claiming a process improvement.
