#!/usr/bin/env python3
"""Report and sync third-party skills tracked by the root registry."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_REGISTRY = REPO_ROOT / "skills-registry.json"
INSTALLER = REPO_ROOT / "skill-installer" / "scripts" / "install-skill-from-github.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report or sync third-party skills tracked in skills-registry.json."
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Path to the root-level skills registry JSON file.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report current registry status without making changes.",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Update all selected third-party skills by reinstalling them from their configured source.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Limit reporting or sync to one skill. Repeat for multiple skills.",
    )
    return parser.parse_args()


def load_registry(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or "entries" not in data:
        raise ValueError(f"Invalid registry format: {path}")
    if not isinstance(data["entries"], list):
        raise ValueError(f"Registry entries must be a list: {path}")
    return data


def filter_entries(entries: list[dict], selected: set[str]) -> list[dict]:
    if not selected:
        return entries
    return [entry for entry in entries if entry["name"] in selected]


def ensure_known_selection(entries: list[dict], selected: set[str]) -> None:
    if not selected:
        return
    available = {entry["name"] for entry in entries}
    missing = sorted(selected - available)
    if missing:
        raise SystemExit(f"Unknown skill(s) in registry: {', '.join(missing)}")


def local_skill_state(name: str) -> str:
    skill_file = REPO_ROOT / name / "SKILL.md"
    return "present" if skill_file.exists() else "missing"


def source_label(entry: dict) -> str:
    repo = entry.get("source_repo", "")
    path = entry.get("source_path", "")
    if repo and path:
        return f"{repo}:{path}"
    if repo:
        return repo
    return entry.get("source_type", "unknown")


def print_report(entries: list[dict]) -> None:
    counts = Counter(entry["ownership"] for entry in entries)
    print("Skill Ownership Summary")
    print(f"  total={len(entries)} third_party={counts.get('third_party', 0)} first_party={counts.get('first_party', 0)} unknown={counts.get('unknown', 0)}")
    print("")
    for entry in entries:
        print(
            f"- {entry['name']}: ownership={entry['ownership']} state={local_skill_state(entry['name'])} "
            f"source={source_label(entry)} sync_method={entry['sync_method']}"
        )


def validate_syncable(entry: dict) -> None:
    if entry["ownership"] != "third_party":
        raise ValueError(f"{entry['name']} is not marked as third_party")
    if entry["source_type"] != "github":
        raise ValueError(f"{entry['name']} is not configured for github sync")
    if not entry.get("source_repo") or not entry.get("source_path"):
        raise ValueError(f"{entry['name']} is missing source_repo or source_path")


def sync_entry(entry: dict) -> None:
    validate_syncable(entry)
    target_dir = REPO_ROOT / entry["name"]
    with tempfile.TemporaryDirectory(prefix=f"sync-skill-{entry['name']}-") as tmp:
        tmpdir = Path(tmp)
        cmd = [
            sys.executable,
            str(INSTALLER),
            "--repo",
            entry["source_repo"],
            "--ref",
            entry.get("source_ref", "main"),
            "--path",
            entry["source_path"],
            "--dest",
            str(tmpdir),
            "--name",
            entry["name"],
        ]
        subprocess.run(cmd, check=True)
        staged_dir = tmpdir / entry["name"]
        staged_skill = staged_dir / "SKILL.md"
        if not staged_skill.exists():
            raise FileNotFoundError(f"Synced skill is missing SKILL.md: {staged_skill}")
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(staged_dir, target_dir)


def main() -> int:
    args = parse_args()
    if not args.check and not args.sync:
        args.check = True
    if args.check and args.sync:
        raise SystemExit("Choose either --check or --sync, not both.")
    if not INSTALLER.exists():
        raise SystemExit(f"Installer helper not found: {INSTALLER}")

    registry = load_registry(args.registry)
    entries = registry["entries"]
    selected = set(args.skill)
    ensure_known_selection(entries, selected)
    entries = filter_entries(entries, selected)

    if args.check:
        print_report(entries)
        return 0

    syncable = [entry for entry in entries if entry["ownership"] == "third_party"]
    skipped = [entry for entry in entries if entry["ownership"] != "third_party"]
    print_report(entries)
    print("")
    for entry in skipped:
        print(f"SKIP {entry['name']}: ownership={entry['ownership']}")
    for entry in syncable:
        print(f"SYNC {entry['name']}: {source_label(entry)}")
        sync_entry(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
