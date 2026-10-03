#!/usr/bin/env python3
"""Check that the lean playbook keeps its essential files and links."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "AGENTS.md", "VERSION", "docs/workflow.md", "docs/adoption.md",
    "skills/initialize-ai-native-project/SKILL.md",
    "skills/initialize-ai-native-project/scripts/initialize_project.py",
    "skills/initialize-ai-native-project/scripts/validate_project.py",
    "skills/initialize-ai-native-project/assets/project-starter/project/docs/development-workflow.md",
    "skills/initialize-ai-native-project/assets/project-starter/change/intent.md",
    "skills/initialize-ai-native-project/assets/project-starter/change/spec.md",
    "skills/initialize-ai-native-project/assets/project-starter/change/plan.md",
    "skills/initialize-ai-native-project/references/document-guide.md",
)


def main() -> int:
    missing = [relative for relative in REQUIRED if not (ROOT / relative).is_file()]
    if missing:
        for relative in missing:
            print(f"ERROR: Missing {relative}")
        return 1
    print("Playbook validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
