"""Exercise the validator through its CLI against small real repositories."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_requirements.py"
SHA = "a" * 40
DRAFT = """# TEST-001 — Change a behaviour
Status: Draft
Owner: Product Lead
Product acceptance: Not accepted

## Required behaviour
| ID | Requirement | Decision |
| --- | --- | --- |
| FR-001 | The system must display the result. | D-001 |

## Acceptance examples
| ID | Requirement | Starting state | Action | Expected result |
| --- | --- | --- | --- | --- |
| EX-001 | FR-001 | A valid input | Submit | Result displayed |

## Confirmed decisions
| ID | Decision | Status |
| --- | --- | --- |
| D-001 | Display the result. | Confirmed |
"""
READY = DRAFT.replace("Status: Draft", "Status: Ready for engineering").replace(
    "Product acceptance: Not accepted",
    """Product acceptance: Accepted
Accepted by: Product Lead
Accepted on: 2026-10-25
Accepted scope: FR-001, EX-001
Acceptance evidence: Recorded product-owner confirmation in this fixture.
Material blockers: None""",
)
HANDOFF = f"""
## Implementation
Handoff status: Prepared
Requirements baseline commit SHA: {SHA}
Platform evidence commit SHA: {'b' * 40}
Pinned requirements link: https://github.com/example/requirements/blob/{SHA}/capabilities/test/requirements.md
Pinned decisions link: https://github.com/example/requirements/blob/{SHA}/capabilities/test/requirements.md
Included IDs: FR-001, EX-001
"""


class ValidatorCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def run_validator(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)],
            capture_output=True, text=True, check=False,
        )

    def check(self, text, code=None):
        self.write("capabilities/test/requirements.md", text)
        result = self.run_validator()
        if code is None:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Structural validation passed", result.stdout)
        else:
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn(code, result.stdout)

    def test_draft_allows_unresolved_work_and_unpinned_handoff(self):
        self.check(DRAFT + "\nMaterial blockers: Q-001\nRequirements baseline commit SHA: Not pinned\n")

    def test_missing_capability_requirements_is_reported(self):
        self.write("capabilities/test/checkpoint.md", "# Still preparing\n")
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing-requirements", result.stdout)

    def test_split_records_resolve_decisions_in_the_same_capability(self):
        requirement, decision = DRAFT.split("## Confirmed decisions")
        self.write("capabilities/test/decisions.md", "# Decisions\n" + decision)
        self.check(requirement)

    def test_duplicate_declaration_is_rejected_but_repeated_mentions_are_valid(self):
        self.check(DRAFT + "\nFR-001 is also discussed here.\n")
        self.check(DRAFT + "\n| ID | Requirement | Decision |\n| --- | --- | --- |\n"
                   + "| FR-001 | Duplicate obligation | D-001 |\n", "duplicate-id")

    def test_coverage_tables_reference_ids_without_redeclaring_them(self):
        self.write("capabilities/test/implementation.md", """# Coverage
| FR / BR | Acceptance examples | Evidence |
| --- | --- | --- |
| FR-001 | EX-001 | Not implemented |
""")
        self.check(DRAFT)

    def test_missing_decision_and_example_references_are_rejected(self):
        for old, new in [("| D-001 |\n", "| D-009 |\n"),
                         ("| EX-001 | FR-001 |", "| EX-001 | FR-009 |")]:
            with self.subTest(reference=new):
                self.check(DRAFT.replace(old, new, 1), "unknown-id")

    def test_ranges_check_the_missing_middle_id(self):
        text = DRAFT.replace("| D-001 |\n", "| D-001–D-003 |\n", 1)
        self.check(text + "\n| ID | Decision | Status |\n| --- | --- | --- |\n"
                   + "| D-003 | Another decision | Confirmed |\n", "unknown-id")

    def test_retained_superseded_decisions_remain_referenceable(self):
        self.check(DRAFT.replace("| Confirmed |", "| Superseded; see D-002 |")
                   + "| D-002 | Replacement | Confirmed |\n")

    def test_capabilities_have_independent_id_namespaces(self):
        self.write("capabilities/other/requirements.md", DRAFT)
        self.check(DRAFT)

    def test_explicit_cross_capability_reference_uses_target_namespace(self):
        self.write("capabilities/other/requirements.md", DRAFT)
        self.check(DRAFT.replace("| D-001 |\n", "| other:D-001 |\n", 1))
        self.check(DRAFT.replace("| D-001 |\n", "| other:D-099 |\n", 1), "unknown-id")

    def test_missing_local_path_is_rejected_and_external_links_are_not_fetched(self):
        self.check(DRAFT + "\n[Source](https://example.invalid/unavailable)\n")
        self.check(DRAFT + "\n[Missing](missing.md)\n", "broken-link")

    def test_fragments_and_duplicate_heading_slugs(self):
        self.write("guide.md", "# Guide\n## A section\n## A section\n")
        self.check(DRAFT + "\n[Guide](../../guide.md#a-section-1)\n")
        self.check(DRAFT + "\n[Guide](../../guide.md#missing)\n", "broken-fragment")

    def test_fenced_and_inline_code_are_not_interpreted_as_links_or_rows(self):
        self.check(DRAFT + "\n```md\n[missing](missing.md)\n| FR-999 | D-999 |\n```\n"
                   + "\n`[literal](missing.md)`\n")

    def test_templates_are_not_active_capabilities(self):
        self.write("templates/capability/requirements.md", "Status: Ready for engineering\n")
        self.check(DRAFT)

    def test_ready_requires_acceptance_metadata_and_examples(self):
        self.check(READY)
        for text in [
            DRAFT.replace("Status: Draft", "Status: Ready for engineering"),
            READY.replace("Accepted by: Product Lead", "Accepted by: To record"),
            READY.replace("Accepted on: 2026-10-25", "Accepted on: 2026-02-30"),
            READY.replace("Acceptance evidence: Recorded product-owner confirmation in this fixture.", ""),
            READY.replace("| EX-001 | FR-001 | A valid input | Submit | Result displayed |", ""),
        ]:
            with self.subTest(text=text[:80]):
                self.check(text, "readiness")

    def test_ready_rejects_material_blockers(self):
        self.check(READY.replace("Material blockers: None", "Material blockers: Q-001"), "readiness")

    def test_open_question_blocks_only_its_declared_scope(self):
        question = """
## Open questions
| ID | Question | Status | Blocks |
| --- | --- | --- | --- |
| Q-001 | A future choice | Open | FR-002 |
| FR-002 | A separately confirmed future obligation | D-001 | Not selected |
"""
        self.check(READY + question)
        self.check(READY + question.replace("| Open | FR-002 |", "| Open | FR-001 |"), "readiness")

    def test_missing_or_unknown_readiness_status_is_not_silently_skipped(self):
        self.check(DRAFT.replace("Status: Draft\n", ""), "status")
        self.check(DRAFT.replace("Status: Draft", "Status: Complete"), "status")

    def test_prepared_compact_and_split_handoffs_pass(self):
        self.check(READY + HANDOFF)
        self.write("capabilities/test/implementation.md", "# Handoff\n" + HANDOFF)
        self.check(READY)

    def test_prepared_handoff_rejects_draft_or_unpinned_or_mismatched_baseline(self):
        for text in [DRAFT + HANDOFF, READY + HANDOFF.replace(SHA, "Not pinned", 1),
                     READY + HANDOFF.replace(f"blob/{SHA}/", f"blob/{'c' * 40}/", 1),
                     READY + HANDOFF.replace("Included IDs: FR-001, EX-001", "Included IDs: FR-002")]:
            with self.subTest(text=text[-200:]):
                self.check(text, "handoff")

    def test_delivery_in_progress_requires_a_prepared_handoff(self):
        self.check(READY + "\nDelivery state: In progress\n", "handoff")

    def test_deferred_questions_still_block_their_accepted_scope_in_both_layouts(self):
        future = "\n## Future obligation\n| ID | Requirement | Decision |\n| --- | --- | --- |\n| FR-002 | A future outcome | D-001 |\n"
        question = "\n## Questions\n| ID | Question | Status | Blocks |\n| --- | --- | --- | --- |\n| Q-001 | A future choice | Deferred | FR-002 |\n"
        for split in (False, True):
            with self.subTest(split=split):
                if split:
                    self.write("capabilities/test/decisions.md", question)
                    self.check(READY + future + HANDOFF)
                    for blocks in ("FR-001", "All"):
                        self.write("capabilities/test/decisions.md", question.replace("Deferred | FR-002", f"Deferred | {blocks}"))
                        self.check(READY + future + HANDOFF, "readiness")
                else:
                    self.check(READY + future + question + HANDOFF)
                    for blocks in ("FR-001", "All"):
                        self.check(READY + future + question.replace("Deferred | FR-002", f"Deferred | {blocks}") + HANDOFF, "readiness")

    def test_pinned_link_checks_actual_destination_for_both_fields(self):
        for label in ("Pinned requirements link", "Pinned decisions link"):
            line = next(line for line in HANDOFF.splitlines() if line.startswith(label + ":"))
            good = line.split(": ", 1)[1]
            wrong = good.replace(SHA, "c" * 40)
            with self.subTest(field=label):
                self.check(READY + HANDOFF.replace(line, f"{label}: [Accepted record]({good})"))
                self.check(READY + HANDOFF.replace(line, f"{label}: [{good}]({wrong})"), "handoff")
                self.check(READY + HANDOFF.replace(line, f"{label}: https://example.invalid/?next={good}"), "handoff")

    def test_handoff_requires_obligations(self):
        self.check(READY + HANDOFF.replace("Included IDs: FR-001, EX-001", "Included IDs: EX-001"), "handoff")

    def test_scope_cannot_include_decision_question_or_evidence_ids(self):
        for kind in ("D-001", "Q-001", "E-001"):
            extra = "" if kind == "D-001" else f"\n## Other records\n| ID | Record |\n| --- | --- |\n| {kind} | Declared record |\n"
            text = READY.replace("Accepted scope: FR-001, EX-001", f"Accepted scope: FR-001, EX-001, {kind}")
            self.check(text + extra + HANDOFF.replace("Included IDs: FR-001, EX-001", f"Included IDs: {kind}, EX-001"), "readiness")

    def test_business_rule_only_slice_can_have_a_scoped_handoff(self):
        self.check((READY + HANDOFF).replace("FR-001", "BR-001"))

    def test_real_compact_template_supports_table_evidence_references(self):
        template = (SCRIPT.parents[1] / "templates/compact-requirements.md").read_text(encoding="utf-8")
        evidence_header = "| ID | Finding / type | Source / commit / path | Conflict / gap |\n| --- | --- | --- | --- |"
        # Fill the public template's declared evidence interface, then reference it.
        template = template.replace(evidence_header, evidence_header + "\n| E-001 | Documented intent | Fixture source v1 | None |")
        requirement_header = "| ID | Requirement or rule | Decision / shared rule |\n| --- | --- | --- |"
        template = template.replace(requirement_header, requirement_header + "\n| FR-001 | Display the result. | E-001 |")
        self.check(template)


if __name__ == "__main__":
    unittest.main()
