# Evaluate the requirements partner

[cases.json](cases.json) contains fictional inputs and observable rubrics for the workflow. They are not approved product requirements or numerical oracles. The cases cover decision reuse, code/policy conflicts, missing calculation/allocation rules, bounded engineering choices, scoped readiness and access gaps.

## Run a behavioural evaluation

1. Use the actual current `AGENTS.md` and relevant shared standards as the responding agent's instructions. Record their repository commit or identify an uncommitted working tree honestly.
2. Start an independent context for each case where possible. Give it only the case ID, context and task. Do not provide `classification`, `must_do`, `must_not_do` or `critical_checks`; these belong to the grader. Do not add coaching that gives away the expected answer.
3. Save the exact input, response, model/tool identity where available, instruction baseline and date. Avoid tools that modify target platforms or send messages. The cases need no application runtime.
4. In a separate grading pass, compare each response with its rubric. For each dimension below, score `0` = absent/wrong, `1` = partial, `2` = clear and supported. Cite response evidence; record disagreements or `Unknown` rather than infer missing evidence.
5. Mark a case `Pass` only if every critical check holds and every dimension scores `2`. Otherwise record `Needs work` and the specific gap. Do not hide a critical failure in an average score.

| Dimension | Observable question |
| --- | --- |
| Grounding and authority | Are applicable decisions and source limits used correctly? |
| Decision economy | Does the response escalate material choices and avoid answered or bounded engineering questions? |
| Completeness | Does it expose the missing rule or next useful investigation and its consequences? |
| State and scope integrity | Are proposals, acceptance, readiness and implementation authority kept distinct? |

Use a human expert to calibrate model grading before treating scores as a release gate. Author walkthroughs and model-only scores are provisional. Record who responded and who graded; a fresh agent is not a human product approver. Compare the same cases across instruction versions before making improvement claims. Add cases from observed failures and reserve some unseen cases to reduce overfitting.

## Automated checks are separate

`python3 -m unittest discover -s tests -v` validates the dataset's shape, unique case IDs and category coverage. It does not run a model or grade its responses. `python3 scripts/validate_requirements.py` checks repository structure. Neither command is a behavioural evaluation, independent calculation check or acceptance of product scope.

Use the **Evaluate the requirements workflow** prompt in [session prompts](../prompts/session-prompts.md). No paid API runner or always-running orchestration service is included. Store human/model evaluation reports under `evals/results/`, with limitations and responses linked. Keep evaluation results out of normative capability requirements.
