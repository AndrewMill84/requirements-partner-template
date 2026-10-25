# Project context

Owner and product decision authority: To configure (e.g. Product Manager / Domain Lead)
Requirements repository: https://github.com/<org>/<requirements-repo>
Target implementation repository: https://github.com/<org>/<target-platform-repo>
Purpose: Define concise, confirmed functional behaviour and acceptance examples that engineers or AI implementation agents implement in the target platform.
Business domain: To configure (e.g. SaaS platform, B2B workflow, financial/transactional system).
Calculation / regulated domain module required by default: Establish per capability (see [standards/domain-calculations-module.md](standards/domain-calculations-module.md)).
Jurisdictions, currencies and additional stakeholder authorities: Establish per capability (e.g. Operations, Engineering Architecture, Security, Legal/Compliance, Finance).
Local checkouts: Environment-specific; suggested sibling folders `<requirements-repo>/` and `<target-platform-repo>/`. A documented path does not automatically grant access.

## Connected data sources
Configure the repositories, documentation spaces and trackers the requirements agent should inspect during [data-source sync](standards/data-source-sync.md) and capability discovery:

| Source ID | Source type | Location / path / MCP / URL | Authority level | Last synced commit / version / date | Access status |
| --- | --- | --- | --- | --- | --- |
| `SRC-CODE` | Target codebase & tests | `../<target-platform-repo>` or `<org>/<target-platform-repo>` | Current behaviour / implementation constraint | Not yet synced | To verify |
| `SRC-ADR` | Architecture Decision Records (ADRs) | `../<target-platform-repo>/docs/adr/` | Confirmed architectural constraint / documented intent | Not yet synced | To verify |
| `SRC-DOCS` | Product / domain docs & specs | `../<target-platform-repo>/docs/` or wiki/MCP | Documented intent (verify against code & decisions) | Not yet synced | To verify |
| `SRC-TRACKER` | Issue tracker / local implementation specs | Issue tracker URL / MCP or local ticket path | Delivery tracking & historical context | Not yet synced | To verify |

## System orientation
Last synced: Not yet synced (run the **Bootstrap & sync data sources** prompt in [prompts/session-prompts.md](prompts/session-prompts.md) following [standards/data-source-sync.md](standards/data-source-sync.md)).
Sources inspected: None yet.
Note: Orientation is a navigation map, not an executed validation of runtime behaviour or a full code audit.

| Area | Target system reference | Notes / conventions |
| --- | --- | --- |
| Core domain logic | To populate during data-source sync | |
| Application commands, workflows or services | To populate during data-source sync | |
| Schemas, contracts and events | To populate during data-source sync | |
| Read models, projections or reporting | To populate during data-source sync | |
| API and user interface | To populate during data-source sync | |
| Vocabulary and architecture decisions | To populate during data-source sync | |
| Implementation tickets and specs | To populate during data-source sync | |
| Automated tests and known issues | To populate during data-source sync | |

Recheck relevant code, tests and authoritative documents for each capability. Documentation may conflict with code or become stale; do not import product rules from this high-level table without checking the underlying source.

## Authority and boundaries
Confirmed requirements in this repository define agreed target behaviour for their stated scope. Target system ADRs and specifications establish existing constraints and documented intent. Conflicts require an explicit decision and coordinated documentation change; this repository does not silently override locked ADRs.

The target repository's `AGENTS.md` governs work in the implementation checkout. This repository's [AGENTS.md](AGENTS.md) governs requirements discovery and specification work.

No product policy defaults are established merely by linking the repositories or syncing data sources.

## Collaboration
Use reviewable commits and preserve existing work. For repository improvements or scoped requirement changes, open an issue or ticket first (where used), create a dedicated feature branch, run the offline validation checks (`python3 scripts/validate_requirements.py` and `python3 -m unittest discover -s tests -v`), and open a pull request for review before merging into `main`. Product acceptance of requirements does not itself authorise merging, deployment or unrelated application changes.

See [standards/delivery-workflow.md](standards/delivery-workflow.md) for the handoff contract.
