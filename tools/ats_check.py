#!/usr/bin/env python3
"""Basic ATS text-layer check for generated PDFs."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


SECTION_HEADINGS = [
    "experience",
    "education",
    "skills",
    "projects",
    "certifications",
    "publications",
]


def extract_text(pdf_path: Path) -> tuple[int, str, str]:
    if not shutil.which("pdftotext"):
        return 3, "", "pdftotext is not installed; install Poppler to run ATS extraction."
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=30,
    )
    return result.returncode, result.stdout or "", result.stderr.strip()


def read_profile_contact(root: Path) -> list[str]:
    profile = root / "profile" / "01-candidate-profile.md"
    if not profile.is_file():
        return []
    text = profile.read_text(encoding="utf-8", errors="replace")
    contacts = []
    contacts.extend(re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text))
    contacts.extend(re.findall(r"\+?\d[\d\s().-]{7,}\d", text))
    return [c.strip() for c in contacts if "[" not in c and "YOUR_" not in c]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether a PDF has extractable ATS-readable text.")
    parser.add_argument("pdf", help="Path to PDF")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], help="Repository root")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    if not pdf_path.is_file():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    code, text, error = extract_text(pdf_path)
    if code == 3:
        print(f"SKIP: {error}")
        return 0
    if code != 0:
        print(f"ERROR: pdftotext failed: {error}", file=sys.stderr)
        return code or 1

    warnings = []
    normalized = text.strip()
    if not normalized:
        warnings.append("Extracted text is empty.")
    if "(cid:" in text or "\ufffd" in text:
        warnings.append("Extracted text contains replacement or CID markers.")

    lower = text.lower()
    found_headings = [heading for heading in SECTION_HEADINGS if heading in lower]
    if not found_headings:
        warnings.append("No common CV section headings were found in extracted text.")

    contacts = read_profile_contact(Path(args.root).resolve())
    missing_contacts = [contact for contact in contacts if contact not in text]
    if missing_contacts:
        warnings.append("Profile contact fields not found in extracted text: " + ", ".join(missing_contacts))

    print(f"Extracted characters: {len(text)}")
    print("Headings found: " + (", ".join(found_headings) if found_headings else "none"))

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
        return 1

    print("OK: PDF text layer is extractable and basic checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
