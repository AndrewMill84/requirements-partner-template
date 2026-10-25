#!/usr/bin/env python3
"""Validate prospective observations and report coverage-aware workflow measures."""

import argparse
from collections import defaultdict
from datetime import date
import json
import math
from pathlib import Path
import re


UNKNOWN = {"minutes": None, "method": "unknown", "source": None}
SHA = re.compile(r"[0-9a-f]{40}")
SCOPE_ID = re.compile(r"(?:FR|BR|EX)-\d{3,}")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def iso_date(value):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value), "date must be YYYY-MM-DD")
    date.fromisoformat(value)


def effort(value):
    require(isinstance(value, dict), "effort must be an object")
    minutes = value.get("minutes")
    method = value.get("method")
    if minutes is None:
        require(method == "unknown" and value.get("source") is None, "unknown effort needs null minutes/source and method unknown")
    else:
        require(type(minutes) in (int, float) and math.isfinite(minutes) and minutes >= 0, "effort minutes must be finite, non-negative numbers")
        require(method in {"timer", "human_estimate"} and text(value.get("source")), "known effort needs a timer/human_estimate and evidence source")


def scope(value, handoff=False):
    require(isinstance(value, list) and all(isinstance(x, str) and SCOPE_ID.fullmatch(x) for x in value), "scope must contain explicit FR/BR/EX IDs")
    require(len(value) == len(set(value)), "scope IDs must not repeat")
    if handoff:
        require(any(x.startswith(("FR-", "BR-")) for x in value) and any(x.startswith("EX-") for x in value), "handoff scope needs an obligation and an example")


def reviewer(value, required=True):
    actor = value.get("reviewer_type")
    if not required and actor is None:
        require(value.get("reviewer") is None, "unknown review must not name a reviewer")
        return
    require(actor in {"human", "agent"} and text(value.get("reviewer")), "judgment needs reviewer_type human/agent and a reviewer")


def validate_record(data, root, name):
    require(isinstance(data, dict), "measurement record must be an object")
    require(type(data.get("schema_version")) is int and data["schema_version"] == 1, "schema_version must be 1")
    capability = data.get("capability")
    require(isinstance(capability, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]*", capability), "invalid capability slug")
    require(name == capability and (root / "capabilities" / capability / "requirements.md").is_file(), "record must match an existing capability and filename")
    iso_date(data.get("tracking_started_on"))
    require(text(data.get("history_note")), "history_note must describe coverage and baseline limits")
    context = data.get("context")
    require(isinstance(context, dict), "context must be an object")
    require(context.get("size") in {"small", "medium", "large", "unknown"}, "invalid task size")
    require(context.get("novelty") in {"low", "medium", "high", "unknown"}, "invalid novelty")
    require(context.get("financial") is None or type(context["financial"]) is bool, "financial must be bool or null")
    require(text(context.get("basis")), "context needs a classification basis")
    seen = set()

    def observation(item):
        require(isinstance(item, dict), "observation must be an object")
        key = item.get("id")
        require(text(key) and key not in seen, "observation/question IDs must be non-empty and unique within a capability")
        seen.add(key)
        iso_date(item.get("date"))
        require(text(item.get("evidence")), "observation needs evidence")

    for key in ("sessions", "findings", "handoff_reviews"):
        require(isinstance(data.get(key), list), f"{key} must be a list; empty means no recorded observations")
    for item in data["sessions"]:
        observation(item)
        commit = item.get("workflow_commit")
        require(commit is None or isinstance(commit, str) and SHA.fullmatch(commit), "workflow_commit must be a full SHA or null")
        require(item.get("agent") is None or text(item["agent"]), "agent must be an identity or null")
        require(item.get("phase") in {"Preparation", "Decisions", "Reconciliation", "Behaviour review", "Handoff", "Followup"}, "invalid workflow phase")
        scope(item.get("scope"))
        effort(item.get("human_effort"))
        effort(item.get("recording_effort", UNKNOWN))
        capture, questions = item.get("question_capture"), item.get("questions")
        require(capture in {"complete", "partial", "unknown"}, "invalid question capture status")
        require((capture == "unknown" and questions is None) or
                (capture in {"complete", "partial"} and isinstance(questions, list)), "question list and capture status disagree")
        feedback = item.get("human_feedback")
        require(feedback is None or isinstance(feedback, dict) and text(feedback.get("text")) and text(feedback.get("source")), "human_feedback needs text and a human source, or null")
        for question in questions or []:
            require(isinstance(question, dict), "question must be an object")
            key = question.get("id")
            require(text(key) and key not in seen, "observation/question IDs must be non-empty and unique within a capability")
            seen.add(key)
            require(question.get("kind") in {"business_decision", "evidence_request", "already_answered", "engineering_choice", "other"}, "invalid question kind")
            require(text(question.get("summary")) and text(question.get("evidence")), "question needs summary and evidence")
            verdict = question.get("verdict")
            require(verdict in {"pending", "necessary", "avoidable"}, "invalid question verdict")
            reviewer(question, required=verdict != "pending")
            if verdict != "pending":
                require(text(question.get("review_basis")), "question judgment needs a review basis")
    for item in data["findings"]:
        observation(item)
        require(item.get("stage") in {"discovery", "requirements_review", "implementation", "post_delivery"}, "invalid finding stage")
        require(item.get("cause") in {"requirements_gap", "business_change", "implementation_defect", "external_change", "unknown"}, "invalid finding cause")
        require(item.get("severity") in {"minor", "major", "unknown"} and text(item.get("summary")), "finding needs severity and summary")
        reviewer(item, required=item["cause"] != "unknown")
        scope(item.get("affected_ids"))
        effort(item.get("rework_effort"))
    firsts = set()
    for item in data["handoff_reviews"]:
        observation(item)
        require(isinstance(item.get("baseline_commit"), str) and SHA.fullmatch(item["baseline_commit"]), "handoff baseline must be a full SHA")
        scope(item.get("scope"), handoff=True)
        require(item.get("review") in {"first", "followup"}, "invalid handoff review type")
        require(item.get("result") in {"no_clarification", "clarification_needed", "not_reviewed"}, "invalid handoff result")
        reviewer(item, required=item["result"] != "not_reviewed")
        key = (item["baseline_commit"], tuple(sorted(item["scope"])), item.get("reviewer_type"))
        if item["review"] == "first":
            require(key not in firsts, "duplicate first handoff review for the same baseline/scope/reviewer type")
            firsts.add(key)


def effort_stats(values):
    known = [v for v in values if v["minutes"] is not None]
    return {"known_minutes": sum(v["minutes"] for v in known) if known else None,
            "known_records": len(known), "total_records": len(values),
            "timer_records": sum(v["method"] == "timer" for v in values),
            "estimate_records": sum(v["method"] == "human_estimate" for v in values)}


def question_stats(sessions):
    captured = [s for s in sessions if isinstance(s["questions"], list)]
    questions = [q for s in captured for q in s["questions"]]
    human = [q for q in questions if q["verdict"] != "pending" and q["reviewer_type"] == "human"]
    avoidable = sum(q["verdict"] == "avoidable" for q in human)
    return {"logged": len(questions) if captured else None, "sessions_with_capture": len(captured),
            "complete_capture_sessions": sum(s["question_capture"] == "complete" for s in sessions),
            "human_reviewed": len(human), "human_avoidable": avoidable,
            "human_avoidable_rate": avoidable / len(human) if human else None,
            "agent_avoidable": sum(q["verdict"] == "avoidable" and q["reviewer_type"] == "agent" for q in questions),
            "pending": sum(q["verdict"] == "pending" for q in questions),
            "business_decisions_logged": sum(q["kind"] == "business_decision" for q in questions)}


def summarize(data):
    sessions, findings, reviews = data["sessions"], data["findings"], data["handoff_reviews"]
    firsts = [x for x in reviews if x["review"] == "first" and x["reviewer_type"] == "human" and x["result"] != "not_reviewed"]
    passed = sum(x["result"] == "no_clarification" for x in firsts)
    groups = defaultdict(list)
    for item in sessions:
        groups[item["workflow_commit"]].append(item)
    late = [x for x in findings if x["stage"] in {"implementation", "post_delivery"} and x["cause"] == "requirements_gap"]
    return {"capability": data["capability"], "tracking_started_on": data["tracking_started_on"],
            "context": data["context"], "history_note": data["history_note"], "sessions_recorded": len(sessions),
            "human_effort": effort_stats([x["human_effort"] for x in sessions]),
            "recording_effort": effort_stats([x.get("recording_effort", UNKNOWN) for x in sessions]),
            "questions": question_stats(sessions),
            "findings": {"logged": len(findings), "early_logged": sum(x["stage"] in {"discovery", "requirements_review"} for x in findings),
                         "late_logged": sum(x["stage"] in {"implementation", "post_delivery"} for x in findings),
                         "late_unknown_cause": sum(x["stage"] in {"implementation", "post_delivery"} and x["cause"] == "unknown" for x in findings),
                         "human_late_requirements": sum(x["reviewer_type"] == "human" for x in late),
                         "agent_late_requirements": sum(x["reviewer_type"] == "agent" for x in late),
                         "human_business_changes": sum(x["cause"] == "business_change" and x["reviewer_type"] == "human" for x in findings),
                         "rework_effort": effort_stats([x["rework_effort"] for x in findings]),
                         "requirements_rework_effort": effort_stats([x["rework_effort"] for x in findings if x["cause"] == "requirements_gap" and x["reviewer_type"] == "human"])},
            "handoffs": {"logged": len(reviews), "human_first_reviews": len(firsts), "human_no_clarification": passed,
                         "human_first_pass_rate": passed / len(firsts) if firsts else None,
                         "agent_reviews": sum(x["reviewer_type"] == "agent" for x in reviews)},
            "session_versions": [{"workflow_commit": key, "sessions": len(value),
                                  "agents": sorted({x["agent"] for x in value if x["agent"] is not None}),
                                  "unknown_agent_sessions": sum(x["agent"] is None for x in value),
                                  "human_effort": effort_stats([x["human_effort"] for x in value]),
                                  "questions": question_stats(value)} for key, value in sorted(groups.items(), key=lambda x: x[0] or "")]}


def markdown(records, untracked):
    lines = ["# Requirements workflow observations", "", "Descriptive records are not evidence of improvement on their own.",
             "Unknown is not zero. Logged counts do not prove complete observation or absence of defects.",
             "Untracked capabilities: " + (", ".join(untracked) if untracked else "None"), ""]
    for r in records:
        e, q, f, h = r["human_effort"], r["questions"], r["findings"], r["handoffs"]
        minutes = "Unknown" if e["known_minutes"] is None else f'{e["known_minutes"]:g} known minutes'
        question_count = "Unknown" if q["logged"] is None else str(q["logged"])
        avoidability = "Unknown" if q["human_avoidable_rate"] is None else f'{q["human_avoidable"]}/{q["human_reviewed"]} human-reviewed'
        handoffs = "Unknown" if h["human_first_pass_rate"] is None else f'{h["human_no_clarification"]}/{h["human_first_reviews"]} human-reviewed first handoffs'
        rework = f["requirements_rework_effort"]
        rework_minutes = "Unknown" if rework["known_minutes"] is None else f'{rework["known_minutes"]:g} known minutes'
        overhead = r["recording_effort"]
        overhead_minutes = "Unknown" if overhead["known_minutes"] is None else f'{overhead["known_minutes"]:g} known minutes'
        all_rework = f["rework_effort"]
        all_rework_minutes = "Unknown" if all_rework["known_minutes"] is None else f'{all_rework["known_minutes"]:g} known minutes'
        lines += [f'## {r["capability"]}', "", f'Tracking starts: {r["tracking_started_on"]}; size: {r["context"]["size"]}; novelty: {r["context"]["novelty"]}.',
                  r["history_note"], "", "| Measure | Observed value | Coverage / interpretation |", "| --- | --- | --- |",
                  f'| Human effort | {minutes} | {e["known_records"]}/{e["total_records"]} recorded sessions; {e["timer_records"]} timer, {e["estimate_records"]} estimates |',
                  f'| Recording overhead | {overhead_minutes} | {overhead["known_records"]}/{overhead["total_records"]} recorded sessions; part of total effort, not an extra additive saving |',
                  f'| Questions logged | {question_count} | {q["complete_capture_sessions"]}/{r["sessions_recorded"]} sessions have complete question capture |',
                  f'| Avoidable questions | {avoidability} | {q["agent_avoidable"]} separately agent-flagged; {q["pending"]} pending |',
                  f'| Early findings logged | {f["early_logged"]} | Recorded events only; severity and evidence remain in the source |',
                  f'| Downstream findings logged | {f["late_logged"]} | {f["late_unknown_cause"]} unknown cause; these are not automatically requirements failures |',
                  f'| Late requirements gaps | {f["human_late_requirements"]} human-attributed | {f["agent_late_requirements"]} separately agent-attributed; follow-up coverage is not implied |',
                  f'| All-cause rework logged | {all_rework_minutes} | {all_rework["known_records"]}/{all_rework["total_records"]} findings have effort evidence; includes unknown/business/implementation causes |',
                  f'| Requirements-attributed rework | {rework_minutes} | {rework["known_records"]}/{rework["total_records"]} human-attributed findings have effort evidence |',
                  f'| Handoffs without requirements clarification | {handoffs} | {h["agent_reviews"]} separate agent reviews; does not mean product acceptance |', ""]
        for version in r["session_versions"]:
            v = version["human_effort"]
            known = "Unknown" if v["known_minutes"] is None else f'{v["known_minutes"]:g} known minutes'
            lines.append(f'- Workflow {version["workflow_commit"] or "Unknown"}: {version["sessions"]} sessions; {known} ({v["known_records"]}/{v["total_records"]} covered); agents: {", ".join(version["agents"]) or "Unknown"}; unknown identity: {version["unknown_agent_sessions"]}/{version["sessions"]}.')
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("--root must be an existing repository")
    records, errors = [], []
    for path in sorted((root / "measurements").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            validate_record(data, root, path.stem)
            records.append(summarize(data))
        except (ValueError, TypeError, KeyError, OSError) as error:
            errors.append(f'{path.relative_to(root)}: {error}')
    if errors:
        print("\n".join(errors))
        return 1
    all_capabilities = {path.parent.name for path in (root / "capabilities").glob("*/requirements.md")}
    untracked = sorted(all_capabilities - {record["capability"] for record in records})
    if args.check:
        print(f"Measurement records valid ({len(records)} records). No improvement conclusion inferred.")
        if untracked:
            print("Untracked capabilities: " + ", ".join(untracked))
    elif args.json:
        print(json.dumps({"schema_version": 1, "interpretation": "descriptive_observations_only", "untracked_capabilities": untracked, "records": records}, indent=2))
    else:
        print(markdown(records, untracked), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
