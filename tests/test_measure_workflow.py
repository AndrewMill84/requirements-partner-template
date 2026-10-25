"""Test measurement semantics through real JSON files and the reporting CLI."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/measure_workflow.py"
SHA = "d" * 40
UNKNOWN = {"minutes": None, "method": "unknown", "source": None}
BASE = {
    "schema_version": 1, "capability": "test", "tracking_started_on": "2026-10-25",
    "context": {"size": "small", "novelty": "low", "financial": False, "basis": "Fictional fixture classified before observation."},
    "history_note": "Prospective only; no historical time or questions reconstructed.",
    "sessions": [], "findings": [], "handoff_reviews": [],
}


def session(key="S-001", **changes):
    data = {"id": key, "date": "2026-10-25", "workflow_commit": SHA, "agent": "fixture-agent",
            "phase": "Decisions", "scope": ["FR-001"], "evidence": "Fixture session transcript",
            "human_effort": deepcopy(UNKNOWN), "recording_effort": deepcopy(UNKNOWN),
            "question_capture": "unknown", "questions": None, "human_feedback": None}
    data.update(changes)
    return data


def question(key, verdict, reviewer_type=None):
    return {"id": key, "kind": "business_decision", "summary": "A recorded question",
            "evidence": "Fixture transcript question", "verdict": verdict,
            "reviewer_type": reviewer_type, "reviewer": "Fixture reviewer" if reviewer_type else None,
            "review_basis": "Fixture classification evidence" if reviewer_type else None}


class MeasurementCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "measurements").mkdir()
        capability = self.root / "capabilities/test"
        capability.mkdir(parents=True)
        (capability / "requirements.md").write_text("# Fixture\nStatus: Draft\n", encoding="utf-8")

    def run_report(self, record=None, *args):
        path = self.root / "measurements/test.json"
        path.write_text(json.dumps(BASE if record is None else record), encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *args],
                              capture_output=True, text=True, check=False)

    def summary(self, record):
        result = self.run_report(record, "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)["records"][0]

    def test_no_observations_are_unknown_not_measured_zero(self):
        data = self.summary(BASE)
        self.assertIsNone(data["human_effort"]["known_minutes"])
        self.assertIsNone(data["questions"]["logged"])
        self.assertIsNone(data["questions"]["human_avoidable_rate"])
        self.assertIsNone(data["handoffs"]["human_first_pass_rate"])
        self.assertEqual(data["sessions_recorded"], 0)

    def test_partial_effort_shows_coverage_and_keeps_estimates_distinct(self):
        record = deepcopy(BASE)
        record["sessions"] = [session(human_effort={"minutes": 10, "method": "timer", "source": "Timer record"}),
                              session("S-002", human_effort={"minutes": 20, "method": "human_estimate", "source": "Owner estimate"}),
                              session("S-003")]
        data = self.summary(record)["human_effort"]
        self.assertEqual(data, {"known_minutes": 30, "known_records": 2, "total_records": 3, "timer_records": 1, "estimate_records": 1})

    def test_explicit_zero_and_empty_question_capture_are_observed_values(self):
        record = deepcopy(BASE)
        record["sessions"] = [session(human_effort={"minutes": 0, "method": "human_estimate", "source": "Explicit owner estimate"},
                                      questions=[], question_capture="complete")]
        data = self.summary(record)
        self.assertEqual(data["human_effort"]["known_minutes"], 0)
        self.assertEqual(data["questions"]["logged"], 0)
        self.assertEqual(data["questions"]["complete_capture_sessions"], 1)
        self.assertIsNone(data["questions"]["human_avoidable_rate"])

    def test_question_rate_uses_only_human_reviewed_questions_and_reports_coverage(self):
        record = deepcopy(BASE)
        record["sessions"] = [session(questions=[question("SQ-001", "avoidable", "human"), question("SQ-002", "necessary", "human"),
                                                 question("SQ-003", "avoidable", "agent"), question("SQ-004", "pending")],
                                      question_capture="partial"), session("S-002")]
        data = self.summary(record)["questions"]
        self.assertEqual(data["logged"], 4)
        self.assertEqual(data["human_reviewed"], 2)
        self.assertEqual(data["human_avoidable_rate"], 0.5)
        self.assertEqual(data["agent_avoidable"], 1)
        self.assertEqual(data["complete_capture_sessions"], 0)
        self.assertEqual(data["sessions_with_capture"], 1)

    def test_sessions_are_broken_down_by_workflow_version(self):
        record = deepcopy(BASE)
        record["sessions"] = [session(), session("S-002", workflow_commit="e" * 40)]
        data = self.summary(record)
        self.assertEqual({x["workflow_commit"] for x in data["session_versions"]}, {SHA, "e" * 40})
        self.assertEqual([x["sessions"] for x in data["session_versions"]], [1, 1])

    def test_late_requirements_findings_exclude_business_changes_and_agent_attribution(self):
        record = deepcopy(BASE)
        for key, stage, cause, reviewer in [("F-001", "discovery", "requirements_gap", "human"),
                                            ("F-002", "implementation", "requirements_gap", "human"),
                                            ("F-003", "post_delivery", "business_change", "human"),
                                            ("F-004", "implementation", "requirements_gap", "agent")]:
            record["findings"].append({"id": key, "date": "2026-10-25", "stage": stage, "cause": cause,
                                       "severity": "major", "reviewer_type": reviewer, "reviewer": "Fixture reviewer",
                                       "evidence": "Linked finding", "summary": "Fixture finding", "affected_ids": ["FR-001"],
                                       "rework_effort": deepcopy(UNKNOWN)})
        data = self.summary(record)["findings"]
        self.assertEqual(data["early_logged"], 1)
        self.assertEqual(data["human_late_requirements"], 1)
        self.assertEqual(data["agent_late_requirements"], 1)
        self.assertEqual(data["human_business_changes"], 1)
        self.assertIsNone(data["rework_effort"]["known_minutes"])

    def test_handoff_rate_uses_human_first_reviews_only(self):
        record = deepcopy(BASE)
        for key, review, actor, result in [("H-001", "first", "human", "no_clarification"),
                                           ("H-002", "followup", "human", "no_clarification"),
                                           ("H-003", "first", "agent", "no_clarification")]:
            record["handoff_reviews"].append({"id": key, "date": "2026-10-25", "baseline_commit": key[-1] * 40,
                                              "scope": ["FR-001", "EX-001"], "review": review, "result": result,
                                              "reviewer_type": actor, "reviewer": "Fixture reviewer", "evidence": "Review source"})
        data = self.summary(record)["handoffs"]
        self.assertEqual(data["human_first_reviews"], 1)
        self.assertEqual(data["human_first_pass_rate"], 1.0)
        self.assertEqual(data["agent_reviews"], 1)

    def test_invalid_effort_or_fabricated_attribution_is_rejected(self):
        bad_efforts = [{"minutes": -1, "method": "timer", "source": "Source"},
                      {"minutes": True, "method": "timer", "source": "Source"},
                      {"minutes": 10, "method": "agent_guess", "source": "Source"},
                      {"minutes": 10, "method": "timer", "source": None},
                      {"minutes": None, "method": "timer", "source": "Source"}]
        for effort in bad_efforts:
            with self.subTest(effort=effort):
                record = deepcopy(BASE)
                record["sessions"] = [session(human_effort=effort)]
                self.assertEqual(self.run_report(record, "--check").returncode, 1)
        record["sessions"] = [session(questions=[question("SQ-001", "avoidable")], question_capture="complete")]
        self.assertEqual(self.run_report(record, "--check").returncode, 1)

    def test_duplicate_ids_bad_dates_and_inconsistent_capture_fail(self):
        invalid = [dict(sessions=[session(), session()]),
                   dict(sessions=[session(date="2026-02-30")]),
                   dict(sessions=[session(workflow_commit="main")]),
                   dict(sessions=[session(questions=None, question_capture="complete")]),
                   dict(capability="missing")]
        for changes in invalid:
            with self.subTest(changes=changes):
                record = deepcopy(BASE)
                record.update(changes)
                result = self.run_report(record, "--check")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_markdown_report_discloses_unknowns_and_no_causal_claim(self):
        result = self.run_report(BASE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Unknown", result.stdout)
        self.assertIn("not evidence of improvement", result.stdout)

    def test_rework_is_separated_by_attributed_cause_and_is_visible_in_markdown(self):
        record = deepcopy(BASE)
        for key, cause, minutes in [("F-001", "requirements_gap", 10), ("F-002", "business_change", 60)]:
            record["findings"].append({"id": key, "date": "2026-10-25", "stage": "implementation", "cause": cause,
                                       "severity": "major", "reviewer_type": "human", "reviewer": "Fixture reviewer",
                                       "evidence": "Linked finding", "summary": "Fixture finding", "affected_ids": ["FR-001"],
                                       "rework_effort": {"minutes": minutes, "method": "human_estimate", "source": "Owner estimate"}})
        data = self.summary(record)["findings"]
        self.assertEqual(data["rework_effort"]["known_minutes"], 70)
        self.assertIn("requirements_rework_effort", data)
        self.assertEqual(data["requirements_rework_effort"]["known_minutes"], 10)
        result = self.run_report(record)
        self.assertIn("10 known minutes", result.stdout)

    def test_untracked_capabilities_are_visible_and_malformed_json_fails_cleanly(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("untracked_capabilities", data)
        self.assertEqual(data["untracked_capabilities"], ["test"])
        (self.root / "measurements/test.json").write_text('{"schema_version":', encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_unknown_cause_downstream_rework_stays_visible_without_attributing_failure(self):
        record = deepcopy(BASE)
        record["findings"] = [{"id": "F-001", "date": "2026-10-25", "stage": "implementation", "cause": "unknown",
                               "severity": "major", "reviewer_type": None, "reviewer": None, "evidence": "Implementation issue",
                               "summary": "Correction work with cause pending review", "affected_ids": ["FR-001"],
                               "rework_effort": {"minutes": 120, "method": "timer", "source": "Work timer"}}]
        data = self.summary(record)["findings"]
        self.assertIn("late_unknown_cause", data)
        self.assertEqual(data["late_unknown_cause"], 1)
        self.assertEqual(data["human_late_requirements"], 0)
        self.assertIsNone(data["requirements_rework_effort"]["known_minutes"])
        result = self.run_report(record)
        self.assertIn("120 known minutes", result.stdout)
        self.assertIn("1 unknown cause", result.stdout)

    def test_mixed_agent_identity_coverage_is_explicit(self):
        record = deepcopy(BASE)
        record["sessions"] = [session(), session("S-002", agent=None)]
        data = self.summary(record)["session_versions"][0]
        self.assertIn("unknown_agent_sessions", data)
        self.assertEqual(data["unknown_agent_sessions"], 1)
        result = self.run_report(record)
        self.assertIn("unknown identity: 1/2", result.stdout)


if __name__ == "__main__":
    unittest.main()
