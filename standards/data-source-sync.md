# Syncing to product data sources

Once you set up this repository, the first step is to connect the requirements partner to your product's sources of truth so it can investigate real system constraints, reuse existing architecture decisions and share a single controlled vocabulary.

## 1. Principles of data-source sync
- **Evidence, not automatic policy:** Syncing a codebase, wiki or issue tracker gives the agent evidence of `Current behaviour` and `Documented intent`. It never automatically converts implementation quirks or outdated docs into `Confirmed decision` for new product scope.
- **Pin every source to a version:** Record the exact Git commit SHA, document version or review timestamp whenever syncing or citing a source.
- **Surface conflicts explicitly:** Where code, tests, ADRs and product docs disagree, record the discrepancy in `standards/glossary.md` or the capability's evidence table rather than picking a winner silently.
- **Fail honestly on missing access:** If a configured repository path, MCP server or issue tracker is unreachable, mark its status `Unavailable` in [project-context.md](../project-context.md#connected-data-sources) and record the evidence gap. Never guess directory layouts or domain rules.

## 2. Initial bootstrap sync (run once at setup)
1. **Configure sources in [project-context.md](../project-context.md):**
   - Set the **Owner and product decision authority**, **Requirements repository**, **Target implementation repository**, and **Business domain**.
   - List each code repository, ADR directory, documentation/wiki space, schema registry and issue tracker in the **Connected data sources** table.
2. **Verify access and record versions:**
   - For each source, verify read access and capture its current commit SHA (e.g., `git rev-parse HEAD`) or version/date in the `Last synced commit / version / date` column.
3. **Populate System orientation in [project-context.md](../project-context.md#system-orientation):**
   - Inspect top-level entry points (`README.md`, `AGENTS.md`, `CONTEXT.md`, package/service directories, ADR index, schema folders, test suites and ticket conventions).
   - Map each functional area (domain logic, commands/workflows, schemas, read models, API/UI, ADRs, issue tracking, test suites) to exact paths or references.
   - Do not start application servers or copy runtime setup steps unless explicitly asked.
4. **Populate [standards/glossary.md](glossary.md):**
   - Extract core domain entities, state names, schedule/lifecycle terms and existing rule/invariant identifiers (`RULE-*`, `INV-*`, `ADR-*`, etc.) that appear across capabilities.
   - For each term, record its definition, its status (`Confirmed decision`, `Documented intent`, `Current behaviour`, or `Confirmed decision vs Current behaviour conflict`) and a pinned link or citation to the source.
5. **Review and commit:**
   - Present a concise summary of synced sources, discovered orientation, extracted glossary terms, any code-vs-doc conflicts and any inaccessible sources for owner review.

## 3. Capability-level sync and evidence freshness
When starting or resuming a capability (`capabilities/<slug>/`):
1. **Check source freshness:** Compare the current `HEAD` commit or version of affected data sources against the commit recorded in [project-context.md](../project-context.md) or the capability's `decisions.md` / `checkpoint.md`.
2. **Inspect only affected areas:** Load only the code modules, tests, ADRs and tickets relevant to the capability's scope. Record findings as `E-001`, `E-002`, etc., with exact commit SHAs, file paths and symbol/test names.
3. **Reconcile delta changes:** If target code or ADRs changed since the capability's last session, note whether the change affects any confirmed decision (`D-*`), requirement (`FR-*`/`BR-*`), or open question (`Q-*`).
4. **Update shared glossary sparingly:** When a capability confirms a new cross-cutting domain term or resolves a glossary conflict, update [standards/glossary.md](glossary.md) with a link to the confirmed decision ID (`<capability-slug>:D-001`).
