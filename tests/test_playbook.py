import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "skills/initialize-ai-native-project/scripts/initialize_project.py"
VALIDATE = ROOT / "skills/initialize-ai-native-project/scripts/validate_project.py"


def initialize(target: Path, *extra: str):
    return subprocess.run(
        [sys.executable, str(INIT), str(target), "--project-name", "Moon Garden",
         "--owner", "Product Team", "--project-type", "game", "--problem",
         "Make collaborative storytelling easier", "--target-users", "small groups", *extra],
        text=True, capture_output=True, check=False,
    )


class PlaybookTests(unittest.TestCase):
    def test_empty_project_initializes_and_validates(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            self.assertEqual(initialize(target).returncode, 0)
            self.assertEqual(
                {str(p.relative_to(target)) for p in target.rglob("*") if p.is_file()},
                {"README.md", "AGENTS.md", "docs/development-workflow.md",
                 ".github/pull_request_template.md"},
            )
            self.assertFalse((target / "docs/intent").exists())
            self.assertFalse((target / "docs/product.md").exists())
            self.assertTrue((target / "docs/development-workflow.md").is_file())
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_generated_workflow_contains_full_canonical_policy(self):
        source = ROOT / "skills/initialize-ai-native-project/assets/project-starter/project/docs/development-workflow.md"
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            result = initialize(target, "--initial-work-shape", "expanded")
            self.assertEqual(result.returncode, 0, result.stderr)
            expected = source.read_text()
            self.assertEqual((target / "docs/development-workflow.md").read_text(), expected)
            self.assertFalse((target / "skills").exists())

    def test_existing_files_are_preserved_with_proposals(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            target.mkdir()
            (target / "AGENTS.md").write_text("existing\n")
            result = initialize(target, "--adopt-existing")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((target / "AGENTS.md").read_text(), "existing\n")
            self.assertTrue((target / "AGENTS.md.playbook-proposed").is_file())

    def test_nonempty_project_requires_adoption(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            target.mkdir()
            (target / "keep.txt").write_text("keep")
            self.assertNotEqual(initialize(target).returncode, 0)

    def test_initializer_rejects_managed_symlink(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            target = root / "product"
            outside = root / "outside"
            target.mkdir(); outside.mkdir()
            (target / "docs").symlink_to(outside, target_is_directory=True)
            result = initialize(target, "--adopt-existing")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(outside.iterdir()), [])

    def test_compact_and_expanded_intents_validate(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            initialize(target)
            compact = target / "docs/intent/INT-001-small-fix"
            compact.mkdir(parents=True); (compact / "change.md").write_text("# Change\n")
            expanded = target / "docs/intent/INT-002-feature"
            expanded.mkdir(parents=True); (expanded / "intent.md").write_text("# Intent\n")
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            # Empty content can pass structure checks; success must not imply approval.
            self.assertIn(b"authorization, content and evidence were not verified", result.stdout)

    def test_plan_requires_intent_but_not_separate_spec(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            self.assertEqual(initialize(target).returncode, 0)
            work = target / "docs/intent/INT-003-planned-change"
            work.mkdir(parents=True)
            (work / "intent.md").write_text("# Intent\nScope: update label\nAC-1: shows Begin\n")
            (work / "plan.md").write_text("# Plan\nInputs: INT-003, AC-1\n")
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            (work / "intent.md").unlink()
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b"requires change.md or intent.md", result.stdout)

    def test_rerun_is_idempotent(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            self.assertEqual(initialize(target).returncode, 0)
            before = {p.relative_to(target): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.assertEqual(initialize(target).returncode, 0)
            after = {p.relative_to(target): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_validator_rejects_unresolved_proposal(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            initialize(target)
            (target / "AGENTS.md.playbook-proposed").write_text("proposal\n")
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)

    def test_validator_rejects_symlinked_intent(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            target = root / "product"
            initialize(target)
            outside = root / "outside"
            outside.mkdir(); (outside / "intent.md").write_text("# outside\n")
            (target / "docs/intent").mkdir()
            (target / "docs/intent/INT-003-linked").symlink_to(outside, target_is_directory=True)
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)

    def test_descriptive_feature_validates_without_spec(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            initialize(target)
            feature = target / "docs/intent/video-clipping"
            feature.mkdir(parents=True)
            (feature / "intent.md").write_text("# Video clipping\nStatus: Approved\n")
            (feature / "plan.md").write_text("# Plan\n")
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_review_ready_sections_warn_without_failing(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            initialize(target)
            feature = target / "docs/intent/video-clipping"
            feature.mkdir(parents=True)
            (feature / "intent.md").write_text("# Clipping\n## Owner summary\n")
            (feature / "spec.md").write_text("# Design\n## Behavior\n")
            (feature / "plan.md").write_text("# 计划\n## 负责人摘要\n")
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(b"video-clipping/spec.md has no owner summary heading", result.stdout)
            self.assertIn(b"video-clipping/spec.md has no assumptions heading", result.stdout)
            self.assertNotIn(b"intent.md has no owner summary", result.stdout)
            self.assertNotIn(b"plan.md has no owner summary", result.stdout)
            (feature / "spec.md").write_text("# 设计\n## 1. 一页读懂\n## 10.2 尚未验证的事项\n")
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertNotIn(b"WARNING", result.stdout)

    def test_templates_carry_review_ready_sections(self):
        change = ROOT / "skills/initialize-ai-native-project/assets/project-starter/change"
        for name in ("intent.md", "spec.md", "plan.md"):
            self.assertIn("## Owner summary", (change / name).read_text(), name)
        self.assertIn("assumptions", (change / "spec.md").read_text())
        self.assertIn("riskiest assumption", (change / "plan.md").read_text())
        guide = ROOT / "skills/initialize-ai-native-project/references/document-guide.md"
        self.assertIn("references/document-guide.md",
                      (ROOT / "skills/initialize-ai-native-project/SKILL.md").read_text())
        self.assertTrue(guide.is_file())

    def test_legacy_workflow_is_preserved_without_duplicate(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            (target / "docs").mkdir(parents=True)
            legacy = target / "docs/workflow.md"
            legacy.write_text("Existing approved workflow\n")
            result = initialize(target, "--adopt-existing")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(legacy.read_text(), "Existing approved workflow\n")
            self.assertFalse((target / "docs/development-workflow.md").exists())
            self.assertTrue((target / "docs/workflow.md.playbook-proposed").is_file())
            self.assertIn("docs/workflow.md", (target / "AGENTS.md").read_text())

    def test_two_workflows_fail_without_changes(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            initialize(target)
            (target / "docs/workflow.md").write_text("Legacy\n")
            before = {p.relative_to(target): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.assertNotEqual(initialize(target, "--adopt-existing").returncode, 0)
            after = {p.relative_to(target): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            result = subprocess.run([sys.executable, str(VALIDATE), str(target)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)

    def test_dangling_legacy_workflow_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "product"
            (target / "docs").mkdir(parents=True)
            (target / "docs/workflow.md").symlink_to(Path(raw) / "missing")
            result = initialize(target, "--adopt-existing")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((target / "docs/development-workflow.md").exists())
            self.assertFalse((target / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
