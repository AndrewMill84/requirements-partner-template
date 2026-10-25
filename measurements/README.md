# Observe whether the requirements workflow improves

Each `measurements/<capability-folder-slug>.json` records task-level observations. The agent maintains it at normal checkpoints and after actual implementation feedback. Requirements, decisions and product acceptance remain authoritative in their existing records; observations reference them rather than redefine them.

The report is generated from the JSON source:

```bash
python3 scripts/measure_workflow.py --check
python3 scripts/measure_workflow.py
python3 scripts/measure_workflow.py --json
```

No model API or dashboard service is required. CI validates records and generates the report. Structural validity does not authenticate a claimed human review or prove an improvement. Empty records mean observation has not begun; missing trackers are listed as untracked capabilities.

## How this relates to current practice

- [Microsoft's SPACE](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/) treats productivity as multidimensional. [EngThrive](https://www.microsoft.com/en-us/research/publication/engthrive-make-it-fast-and-easy-to-do-great-work/), deployed at Microsoft, combines speed, ease and quality with human feedback. Our local adaptation records effort, friction and downstream outcomes together.
- [DORA's AI workflow research](https://dora.dev/insights/balancing-ai-tensions/) describes creation time being reallocated to verification. Include review, correction and recording effort when assessing saved human work; draft speed alone is insufficient.
- [Anthropic measures interventions and clarification stops](https://www.anthropic.com/research/measuring-agent-autonomy/) and explicitly cautions that turn duration is an imperfect proxy. We do not infer active human effort from chat elapsed time or Git timestamps.
- [Requirements-volatility guidance](https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/requirements-volatility/) tracks baseline changes and downstream effects, with no universal cross-industry threshold. Our finding log distinguishes requirements gaps from changed business needs and implementation defects.

These are source-informed local measures, not a standard industry scorecard for AI-written requirements. DORA delivery metrics and requirements gathering measure different parts of the system.

## Measures and denominators

| Question | Recorded evidence | Interpretation |
| --- | --- | --- |
| How much human effort did this take? | Active person-minutes per session, including preparation/review/correction, from a timer or explicit human estimate | Sum known values and show covered sessions. Do not call a partial sum the complete total. Recording overhead is a subset, not an extra additive cost. |
| Which questions needed judgment? | One entry per independent question/decision asked, with kind, evidence and review verdict | Report business-decision questions and logged totals; fewer total questions is not a target by itself. |
| Were questions avoidable? | Necessary/avoidable verdict, reviewer type/name and basis | Human avoidability = human-reviewed avoidable questions / all human-reviewed classified questions. Agent flags and pending items are separate. Show complete/partial capture coverage. |
| Were missing rules found early? | Findings with discovery stage, cause, severity and affected IDs | Early counts are observations, not a reward for finding more issues. Compare cause/severity and follow-up coverage. |
| Did problems escape into implementation? | All implementation/post-delivery findings, including unknown causes | Show total downstream findings and unknown-cause coverage, then separate human-attributed requirements gaps from agent attribution. No logged finding does not establish zero defects. |
| Did requirements cause rework? | Sourced effort against a finding, with reviewed cause | Show all-cause effort even while attribution is pending; human-attributed requirements rework is separate. Missing effort stays unknown. Link fixes/tickets where available. |
| Was the first handoff usable? | First review of a specific baseline and scope | Human-reviewed first handoffs needing no requirements clarification / reviewed human first handoffs. This is not implementation success or product acceptance. |
| Did the process feel easier? | Optional human feedback with a source; recording-overhead estimate where available | Qualitative context; agents must not invent a satisfaction score. |

## Start and maintain a record

Copy [the template](../templates/measurement.json) when beginning a capability or prospectively tracking an existing one. Use the actual tracking start date. Size is `small`/`medium`/`large`/`unknown`; novelty is `low`/`medium`/`high`/`unknown`; financial is `true`/`false`/`null`. Record the classifier and basis before looking at performance. Preserve earlier context changes with an explanation in `history_note`/Git history rather than relabelling difficult work to make results look favourable.

At each substantive requirements checkpoint, append one session record. Amend the same session ID when completing missing evidence; do not count the same work twice. A session is one bounded working period on one capability, not an AI turn or a Git commit. For resumed work, preserve the scope and version actually used. If only part of the conversation is visible, mark capture `partial` or `unknown`.

Session shape (illustrative placeholders, not observed data):

```json
{
  "id": "S-001",
  "date": "YYYY-MM-DD",
  "workflow_commit": null,
  "agent": null,
  "phase": "Preparation",
  "scope": [],
  "evidence": "Observed session/checkpoint/source reference",
  "human_effort": {"minutes": null, "method": "unknown", "source": null},
  "recording_effort": {"minutes": null, "method": "unknown", "source": null},
  "question_capture": "unknown",
  "questions": null,
  "human_feedback": null
}
```

Use the exact loaded instructions commit, not a guessed current SHA. A commit cannot contain its own final SHA; later session records reference the earlier instructions actually used. Agent/model identity remains `null` if unavailable. Phases are `Preparation`, `Decisions`, `Reconciliation`, `Behaviour review`, `Handoff` and `Followup`.

Effort uses finite, non-negative minutes. Known methods are `timer` or `human_estimate`, with a source; unknown uses `null` minutes/source and method `unknown`. Never estimate human activity from response delay, tokens, decision count or the agent's own runtime. A known zero requires actual evidence. Rework uses the same effort shape. Optional `human_feedback` is an object with `text` and `source`, not an agent-invented rating. Do not ask the owner to fill every field: record unknowns and batch optional effort/experience feedback into an existing checkpoint.

Questions use this shape when capture is `complete` or `partial` (an empty list means an observed zero within that coverage):

```json
{
  "id": "S-001-Q-001",
  "kind": "business_decision",
  "summary": "The question actually asked",
  "evidence": "Source or saved question reference",
  "verdict": "pending",
  "reviewer_type": null,
  "reviewer": null,
  "review_basis": null
}
```

Kinds are `business_decision`, `evidence_request`, `already_answered`, `engineering_choice` or `other`. Verdict is `pending`/`necessary`/`avoidable`. A non-pending verdict needs `reviewer_type` (`human`/`agent`), a `reviewer` and `review_basis`. Record `human` only after actual attributable human input; an agent's belief about what the owner would say is `agent` review. Reference the existing `Q` ID in `evidence` where applicable; do not copy the normative decision into this log.

## Findings and handoff feedback

Each finding has `id`, `date`, `evidence`, `summary`, `affected_ids` (`FR`/`BR`/`EX` list, possibly empty before IDs exist), `stage`, `cause`, `severity`, `reviewer_type`, `reviewer` and `rework_effort`. Use stages `discovery`/`requirements_review`/`implementation`/`post_delivery`; causes `requirements_gap`/`business_change`/`implementation_defect`/`external_change`/`unknown`; severity `minor`/`major`/`unknown`. Unknown cause can have `null` reviewer fields; a known attribution needs a named `human` or `agent` reviewer. Preserve the source, rationale and follow-up link in `evidence`/`summary`. Relate multiple symptoms from one root issue to one finding instead of inflating the count.

Each handoff review has `id`, `date`, `evidence`, `baseline_commit` (full SHA), `scope` (`FR`/`BR`/`EX` IDs including an obligation and example), `review` (`first`/`followup`), `result` (`no_clarification`/`clarification_needed`/`not_reviewed`), `reviewer_type` and `reviewer`. Do not log `no_clarification` from silence or a green test suite. Do not duplicate a first review for the same baseline/scope/reviewer type; later feedback is `followup`. The baseline is the immutable requirements baseline, not the target implementation SHA. New business changes do not retroactively turn a valid original requirement into an elicitation failure.

All event/question IDs are unique within the record. All dates are real `YYYY-MM-DD` dates. Evidence can be an immutable repository link, ticket/review reference or a concise saved observation when a permanent transcript link is unavailable. This is a task evidence log, not a mandate to copy entire conversations or unrelated personal details.

## Decide whether the workflow improved

Review after several comparable capabilities, or after a material workflow change. Start with descriptive comparisons, not a single score. Compare similar scope, size, novelty, calculation risk, model and follow-up windows; use the version breakdown rather than silently pooling different workflows. Explain scope changes, missing sessions and reviewer disagreements.
Version summaries show unknown model identities alongside known models; do not treat a partially identified cohort as a single-model result.

Use reliable historical observations only when sources exist; label retrospective estimates. Otherwise start a prospective baseline now and compare future versions. Do not claim that new tracking proves the earlier update improved performance. A few cases can guide adjustments but do not establish statistical or causal improvement.

Look for lower human effort and avoidable friction alongside stable or better late-gap/rework outcomes. Check that review or recording effort has not merely moved the cost elsewhere. Human-review a small sample of classifications to counter agent self-assessment bias. Keep [fixed behavioural evals](../evals/README.md) separate from real-work observations: both are useful, neither substitutes for the other.
