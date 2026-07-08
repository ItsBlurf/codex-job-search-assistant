#!/usr/bin/env python3
"""Readiness checks for the Codex AI Job Search workspace."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_FOLDERS = [
    ".agents/skills",
    "profile",
    "documents/cv",
    "documents/linkedin",
    "documents/diplomas",
    "documents/references",
    "documents/applications",
    "cv",
    "cover_letters",
    "templates",
    "job_scraper/results",
    "tools",
    "tests/smoke",
]

IMPORTANT_COMMANDS = ["python", "pip", "lualatex", "xelatex", "pdftotext", "git"]
OPTIONAL_COMMANDS = ["node", "bun"]


def command_version(command: str) -> tuple[bool, str]:
    exe = shutil.which(command)
    if not exe:
        return False, "not found"
    if command == "pdftotext":
        probes = ([command, "-v"],)
    else:
        probes = ([command, "--version"], [command, "-version"], [command, "-v"])
    for probe in probes:
        try:
            result = subprocess.run(
                probe,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        first = (result.stdout or "").strip().splitlines()
        return True, first[0] if first else exe
    return True, exe


def check_json(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            json.load(handle)
        return True, "valid JSON"
    except FileNotFoundError:
        return False, "missing"
    except json.JSONDecodeError as exc:
        return False, f"invalid JSON: {exc.msg}"


def main() -> int:
    print("Codex AI Job Search setup check")
    print(f"Repository: {ROOT}")
    print()

    py_ok = sys.version_info >= (3, 10)
    print("Python")
    print(f"  {'OK' if py_ok else 'FAIL'} python {sys.version.split()[0]} (requires 3.10+)")
    print()

    missing_folders = []
    print("Folders")
    for folder in EXPECTED_FOLDERS:
        exists = (ROOT / folder).is_dir()
        if not exists:
            missing_folders.append(folder)
        print(f"  {'OK' if exists else 'MISSING'} {folder}")
    print()

    missing_important = []
    print("Important commands")
    for command in IMPORTANT_COMMANDS:
        found, detail = command_version(command)
        if not found and command in {"python", "pip", "git"}:
            missing_important.append(command)
        label = "OK" if found else "MISSING"
        print(f"  {label} {command}: {detail}")
    print()

    print("Optional commands")
    missing_optional = []
    for command in OPTIONAL_COMMANDS:
        found, detail = command_version(command)
        if not found:
            missing_optional.append(command)
        label = "OK" if found else "MISSING"
        print(f"  {label} {command}: {detail}")
    print()

    seen_ok, seen_detail = check_json(ROOT / "job_scraper" / "seen_jobs.json")
    tracker_ok = (ROOT / "job_search_tracker.csv").is_file()
    agents_ok = (ROOT / "AGENTS.md").is_file()
    print("Repository files")
    print(f"  {'OK' if agents_ok else 'MISSING'} AGENTS.md")
    print(f"  {'OK' if tracker_ok else 'MISSING'} job_search_tracker.csv")
    print(f"  {'OK' if seen_ok else 'FAIL'} job_scraper/seen_jobs.json: {seen_detail}")
    print()

    latex_available = any(command_version(cmd)[0] for cmd in ("lualatex", "xelatex"))
    ats_available = command_version("pdftotext")[0]
    bun_available = command_version("bun")[0]

    print("Readiness summary")
    if py_ok and not missing_folders and tracker_ok and seen_ok and agents_ok and not missing_important:
        print("  READY for baseline Codex workflows.")
        exit_code = 0
    else:
        print("  NOT READY for baseline workflows. Fix missing required items above.")
        exit_code = 1

    print(f"  PDF compile: {'available' if latex_available else 'skipped until lualatex/xelatex is installed'}")
    print(f"  ATS extraction: {'available' if ats_available else 'skipped until pdftotext is installed'}")
    print(f"  Portal CLI skills: {'available' if bun_available else 'skipped until Bun is installed'}")
    if missing_optional:
        print(f"  Missing optional commands: {', '.join(missing_optional)}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
