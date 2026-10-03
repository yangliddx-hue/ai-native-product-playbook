#!/usr/bin/env python3
"""Check project structure, not authorization, evidence truth or agent compliance."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED = (
    "AGENTS.md",
)

# Review-ready sections, matched on Markdown headings in English or Chinese.
# Missing sections only warn: small documents stay valid and content quality needs review.
SUMMARY = re.compile(r"summary|摘要|一页读懂", re.IGNORECASE)
ASSUMPTIONS = re.compile(r"assumption|假设|尚未验证", re.IGNORECASE)


def has_symlink(target: Path, path: Path) -> bool:
    current = target
    for part in path.relative_to(target).parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def headings(path: Path) -> list[str]:
    return [line.lstrip("#").strip() for line in path.read_text(errors="replace").splitlines()
            if line.startswith("#")]


def review_warnings(work: Path, names: set[str]) -> list[str]:
    warnings = []
    for name in ("intent.md", "spec.md", "plan.md"):
        if name in names and not any(SUMMARY.search(h) for h in headings(work / name)):
            warnings.append(f"{work.name}/{name} has no owner summary heading")
    if "spec.md" in names and not any(ASSUMPTIONS.search(h) for h in headings(work / "spec.md")):
        warnings.append(f"{work.name}/spec.md has no assumptions heading")
    return warnings


def validate(target: Path) -> tuple[list[str], list[str]]:
    target = target.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not target.is_dir():
        return [f"Target directory does not exist: {target}"], warnings

    workflows = [relative for relative in ("docs/development-workflow.md", "docs/workflow.md")
                 if (target / relative).exists() or (target / relative).is_symlink()]
    if len(workflows) != 1:
        errors.append("Exactly one workflow file is required")
    for relative in (*REQUIRED, *workflows):
        path = target / relative
        if has_symlink(target, path):
            errors.append(f"Managed path contains a symlink: {relative}")
        elif not path.is_file():
            errors.append(f"Missing required file: {relative}")

    proposals = list(target.rglob("*.playbook-proposed"))
    for proposal in proposals:
        errors.append(f"Unresolved proposal: {proposal.relative_to(target)}")

    for root_name in ("docs/intent", "docs/decisions"):
        root = target / root_name
        if root.exists():
            for path in (root, *root.rglob("*")):
                if has_symlink(target, path):
                    errors.append(f"Managed path contains a symlink: {path.relative_to(target)}")

    intent_root = target / "docs/intent"
    if intent_root.is_dir():
        for work in (path for path in intent_root.iterdir() if path.is_dir() and not path.is_symlink()):
            if not re.fullmatch(r"(?:INT-\d{3,}-)?[a-z0-9][a-z0-9-]*", work.name):
                errors.append(f"Invalid Intent directory name: {work.name}")
                continue
            names = {path.name for path in work.iterdir() if path.is_file()}
            if "change.md" in names and names.intersection({"intent.md", "spec.md", "plan.md"}):
                errors.append(f"Compact Intent {work.name} mixes compact and expanded artifacts")
            elif "change.md" not in names and "intent.md" not in names:
                errors.append(f"Intent {work.name} requires change.md or intent.md")
            else:
                warnings.extend(review_warnings(work, names))

    return list(dict.fromkeys(errors)), warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    errors, warnings = validate(args.target)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("Structure validation passed; authorization, content and evidence were not verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
