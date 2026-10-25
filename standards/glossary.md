# Controlled glossary

Populate and maintain this file using [standards/data-source-sync.md](data-source-sync.md) and confirmed decisions across capabilities.

Keep `Confirmed decision`, `Documented intent` and `Current behaviour` distinct. Where target system code or older documentation conflicts with a confirmed product decision, note the conflict explicitly (`Confirmed decision vs Current behaviour conflict`) and cite both sources.

## Core domain entities and states

| Term | Definition | Status | Decision / source |
| --- | --- | --- | --- |
| *Example: Account status* | *Populate during data-source sync or capability discovery. Distinguish internal enum names from user-facing labels.* | *Documented intent / Confirmed decision* | *Cite ADR, source path at commit SHA, or `<capability>:D-001`* |

## Rules, calculations and lifecycle terms

| Term | Definition | Status | Decision / source |
| --- | --- | --- | --- |
| *Example: Effective date vs Recording date* | *Populate when time-sensitive or calculation rules apply.* | *Documented intent / Confirmed decision* | *Cite ADR, source path at commit SHA, or `<capability>:D-001`* |

Add terms only when needed to prevent ambiguity across capabilities. Record deprecated synonyms and their replacements if ambiguity exists. Avoid assuming that terms mean the same thing across different services or repositories.
