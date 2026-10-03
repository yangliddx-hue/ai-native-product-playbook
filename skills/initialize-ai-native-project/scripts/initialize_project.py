#!/usr/bin/env python3
"""Initialize or adopt the AI-Native Product Playbook in a local project."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a local project without creating remote side effects."
    )
    parser.add_argument("target", type=Path)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--project-type", required=True)
    parser.add_argument("--summary", default="Unknown")
    parser.add_argument("--problem", default="Unknown")
    parser.add_argument("--target-users", default="Unknown")
    parser.add_argument("--data-sensitivity", default="Unknown")
    parser.add_argument("--external-side-effects", default="Unknown")
    parser.add_argument("--technical-reviewer", default="Unknown")
    parser.add_argument("--merge-owner", default="Unknown")
    parser.add_argument("--release-owner", default="Unknown")
    parser.add_argument("--setup-command", default="Unknown")
    parser.add_argument("--run-command", default="Unknown")
    parser.add_argument("--test-command", default="Unknown")
    parser.add_argument("--verify-command", default="Unknown")
    parser.add_argument("--build-command", default="Unknown")
    parser.add_argument("--current-stage", default="Unknown")
    parser.add_argument("--environments", default="Unknown")
    parser.add_argument(
        "--initial-work-shape",
        choices=("unknown", "compact", "expanded"),
        default="unknown",
        help="Deprecated compatibility option; document shape is selected when work is known.",
    )
    parser.add_argument("--adopt-existing", action="store_true")
    return parser.parse_args()


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def is_nonempty(path: Path) -> bool:
    return path.exists() and any(path.iterdir())


def already_initialized(path: Path) -> bool:
    return (path / "AGENTS.md").is_file() and any(
        (path / relative).is_file()
        for relative in ("docs/development-workflow.md", "docs/workflow.md")
    )


def reject_managed_symlinks(target: Path, relatives: list[Path]) -> None:
    """Reject existing symlinks in managed paths before making any change."""
    for relative in relatives:
        current = target
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError(
                    f"Managed path contains a symlink: {relative.as_posix()}"
                )


def initialize(args: argparse.Namespace) -> list[str]:
    target = args.target.expanduser().resolve()
    if target.exists() and not target.is_dir():
        raise ValueError(f"Target is not a directory: {target}")

    canonical = Path("docs/development-workflow.md")
    legacy = Path("docs/workflow.md")
    reject_managed_symlinks(target, [canonical, legacy])
    if (target / canonical).exists() and (target / legacy).exists():
        raise ValueError("Both workflow files exist; reconcile the authoritative workflow first")
    workflow_relative = legacy if (target / legacy).exists() else canonical
    initialized = already_initialized(target)
    if is_nonempty(target) and not args.adopt_existing and not initialized:
        raise ValueError(
            "Target directory is not empty. Re-run with --adopt-existing to preserve "
            "existing files and generate merge proposals."
        )

    target.mkdir(parents=True, exist_ok=True)
    skill_root = Path(__file__).resolve().parents[1]
    asset_root = skill_root / "assets/project-starter"
    values = {
        "PROJECT_NAME": args.project_name,
        "PROJECT_SUMMARY": args.summary,
        "OWNER": args.owner,
        "PRODUCT_PROBLEM": args.problem,
        "TARGET_USERS": args.target_users,
        "PROJECT_TYPE": args.project_type,
        "TECHNICAL_REVIEWER": args.technical_reviewer,
        "MERGE_OWNER": args.merge_owner,
        "RELEASE_OWNER": args.release_owner,
        "VERIFY_COMMAND": args.verify_command,
        "SETUP_COMMAND": args.setup_command,
        "RUN_COMMAND": args.run_command,
        "TEST_COMMAND": args.test_command,
        "BUILD_COMMAND": args.build_command,
        "DATA_SENSITIVITY": args.data_sensitivity,
        "EXTERNAL_SIDE_EFFECTS": args.external_side_effects,
        "CURRENT_STAGE": args.current_stage,
        "ENVIRONMENTS": args.environments,
        "WORKFLOW_FILE": workflow_relative.name,
    }

    sources: list[tuple[Path, Path]] = []
    for source in sorted((asset_root / "project").rglob("*")):
        if source.is_file():
            relative = source.relative_to(asset_root / "project")
            sources.append((source, workflow_relative if relative == canonical else relative))
    sources.append(
        (
            asset_root / "github/pull_request_template.md",
            Path(".github/pull_request_template.md"),
        )
    )

    managed_relatives = [relative for _, relative in sources]
    proposal_relatives = [
        relative.with_name(relative.name + ".playbook-proposed")
        for relative in managed_relatives
        if relative.as_posix() != "README.md"
    ]
    managed_relatives.extend(proposal_relatives)
    reject_managed_symlinks(target, managed_relatives)

    actions: list[str] = []
    for source, relative in sources:
        raw_content = source.read_text(encoding="utf-8")
        content = render(raw_content, values)
        if "{{" in content or "}}" in content:
            raise ValueError(f"Unresolved template placeholder in {source}")
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            destination.write_text(content, encoding="utf-8")
            actions.append(f"created {relative.as_posix()}")
            continue
        if destination.read_text(encoding="utf-8") == content:
            actions.append(f"unchanged {relative.as_posix()}")
            continue
        if relative.as_posix() == "README.md":
            actions.append("preserved README.md; generated summary was not applied")
            continue
        proposal = destination.with_name(destination.name + ".playbook-proposed")
        if proposal.exists() and proposal.read_text(encoding="utf-8") == content:
            actions.append(f"unchanged {proposal.relative_to(target).as_posix()}")
        elif proposal.exists():
            actions.append(
                f"preserved stale {proposal.relative_to(target).as_posix()}; reconcile it before refreshing"
            )
        else:
            proposal.write_text(content, encoding="utf-8")
            actions.append(f"proposed {proposal.relative_to(target).as_posix()}")

    return actions


def main() -> int:
    args = parse_args()
    try:
        actions = initialize(args)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print("Local playbook initialization complete. No remote actions were performed.")
    for action in actions:
        print(f"- {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
