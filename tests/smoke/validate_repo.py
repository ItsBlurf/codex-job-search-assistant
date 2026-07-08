#!/usr/bin/env python3
"""Repository smoke tests for the Codex Job Search Assistant."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_SKILLS = [
    "job-setup",
    "profile-expand",
    "job-apply",
    "job-rank",
    "job-scrape",
    "job-upskill",
    "add-job-portal",
    "add-template",
    "record-outcome",
]

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "SETUP.md",
    "LICENSE",
    ".gitignore",
    "assets/codex-job-search-icon.svg",
    "job_search_tracker.csv",
    "job_scraper/seen_jobs.json",
    "tools/setup_check.py",
    "tools/compile_latex.py",
    "tools/ats_check.py",
    "cv/main_example.tex",
    "cover_letters/example_cover_letter.tex",
]

TRACKER_HEADER = [
    "date",
    "company",
    "sector",
    "role",
    "role_type",
    "channel",
    "status",
    "contact_person",
    "fit_rating",
    "notes",
    "cv_file",
    "cover_letter_file",
    "source",
]


class CheckFailure(Exception):
    pass


def run(command: list[str], *, timeout: int = 120, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    if check and result.returncode != 0:
        raise CheckFailure(f"{' '.join(command)} failed with {result.returncode}\n{result.stdout[-4000:]}")
    return result


def assert_exists() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        raise CheckFailure("Missing required files:\n" + "\n".join(missing))

    required_dirs = [
        ".agents/skills",
        "profile",
        "documents/cv",
        "documents/linkedin",
        "documents/diplomas",
        "documents/references",
        "documents/applications",
        "job_scraper/results",
        "templates/cv",
        "templates/cover_letters",
        "tests/smoke",
    ]
    missing_dirs = [path for path in required_dirs if not (ROOT / path).is_dir()]
    if missing_dirs:
        raise CheckFailure("Missing required directories:\n" + "\n".join(missing_dirs))


def assert_skill_frontmatter() -> None:
    errors: list[str] = []
    for name in REQUIRED_SKILLS:
        path = ROOT / ".agents" / "skills" / name / "SKILL.md"
        if not path.exists():
            errors.append(f"{name}: missing SKILL.md")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"{name}: missing YAML front matter")
            continue
        frontmatter = text.split("---", 2)[1]
        if not re.search(r"^name:\s*.+", frontmatter, re.MULTILINE):
            errors.append(f"{name}: missing front matter name")
        if not re.search(r"^description:\s*.+", frontmatter, re.MULTILINE):
            errors.append(f"{name}: missing front matter description")
        if ".claude/" in text and name not in {"profile-expand"}:
            errors.append(f"{name}: contains old .claude path")

    for path in sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"{path}: missing YAML front matter")
            continue
        frontmatter = text.split("---", 2)[1]
        if "name:" not in frontmatter or "description:" not in frontmatter:
            errors.append(f"{path}: missing name or description")

    if errors:
        raise CheckFailure("\n".join(errors))


def assert_json_and_csv() -> None:
    with (ROOT / "job_scraper" / "seen_jobs.json").open(encoding="utf-8") as handle:
        seen = json.load(handle)
    if not isinstance(seen, dict) or "seen" not in seen or not isinstance(seen["seen"], dict):
        raise CheckFailure("job_scraper/seen_jobs.json must be an object with a 'seen' object")

    with (ROOT / "job_search_tracker.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    if header != TRACKER_HEADER:
        raise CheckFailure(f"Unexpected tracker header:\n{header}")


def assert_no_required_claude_dependency() -> None:
    if (ROOT / ".claude").exists():
        raise CheckFailure(".claude directory must not exist in the Codex-native repo")

    forbidden: list[str] = []
    allowed_files = {"validate_repo.py"}
    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts or "node_modules" in path.parts:
            continue
        if path.name in allowed_files:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if ".claude/" in text or ".claude\\" in text:
            forbidden.append(str(path.relative_to(ROOT)))
    if forbidden:
        raise CheckFailure("Unexpected .claude references:\n" + "\n".join(forbidden))


def assert_gitignore() -> None:
    if not shutil.which("git"):
        return
    targets = [
        "documents/cv/private.pdf",
        "documents/linkedin/profile.pdf",
        "documents/diplomas/degree.pdf",
        "documents/references/ref.pdf",
        "documents/applications/acme-role-2026/cv.pdf",
        "cv/generated.pdf",
        "cover_letters/generated.pdf",
        "job_scraper/results/jobs.json",
        "salary_data.json",
        ".env",
    ]
    result = run(["git", "check-ignore", *targets], check=False)
    ignored = {line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()}
    missing = [target for target in targets if target not in ignored]
    if missing:
        raise CheckFailure("These sensitive/generated paths are not gitignored:\n" + "\n".join(missing))


def assert_tool_help() -> None:
    run([sys.executable, "tools/setup_check.py"], timeout=120)
    run([sys.executable, "tools/compile_latex.py", "--help"])
    run([sys.executable, "tools/ats_check.py", "--help"])
    run([sys.executable, "tools/salary_lookup.py", "--help"])


def assert_latex_when_available() -> None:
    if not shutil.which("lualatex") or not shutil.which("xelatex"):
        print("SKIP latex compile: lualatex/xelatex not available")
        return
    run([sys.executable, "tools/compile_latex.py", "cv/main_example.tex", "--engine", "lualatex"], timeout=600)
    run([sys.executable, "tools/compile_latex.py", "cover_letters/example_cover_letter.tex", "--engine", "xelatex"], timeout=600)
    for folder in ("cv", "cover_letters"):
        for pattern in ("*.aux", "*.log", "*.out"):
            for path in (ROOT / folder).glob(pattern):
                path.unlink(missing_ok=True)

    if shutil.which("pdftotext"):
        run([sys.executable, "tools/ats_check.py", "cv/main_example.pdf"], timeout=120)


def assert_bun_portal_smoke() -> None:
    if not shutil.which("bun"):
        print("SKIP portal CLI smoke: bun not available")
        return
    result = run(["bun", "run", ".agents/skills/linkedin-search/cli/src/cli.ts", "--help"], check=False)
    if "USAGE" not in result.stdout or "linkedin-cli" not in result.stdout:
        raise CheckFailure("LinkedIn portal CLI help did not print expected usage")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run smoke checks for this repository.")
    parser.add_argument("--full", action="store_true", help="Run optional compile and portal smoke checks.")
    args = parser.parse_args()

    checks = [
        ("required files", assert_exists),
        ("skill front matter", assert_skill_frontmatter),
        ("json and csv", assert_json_and_csv),
        ("no required claude dependency", assert_no_required_claude_dependency),
        ("gitignore privacy", assert_gitignore),
        ("tool help", assert_tool_help),
    ]
    if args.full:
        checks.extend([
            ("latex and ats", assert_latex_when_available),
            ("portal cli", assert_bun_portal_smoke),
        ])

    for label, check_fn in checks:
        print(f"== {label} ==")
        check_fn()
        print("OK")

    print("All smoke checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckFailure as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
