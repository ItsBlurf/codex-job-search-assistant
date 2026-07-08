#!/usr/bin/env python3
"""Compile a LaTeX file with lualatex or xelatex."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def choose_engine(requested: str | None) -> str | None:
    if requested:
        return requested if shutil.which(requested) else None
    for engine in ("lualatex", "xelatex"):
        if shutil.which(engine):
            return engine
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a .tex file to PDF.")
    parser.add_argument("input", help="Path to the .tex file")
    parser.add_argument("-o", "--output-dir", help="Directory for generated PDF and build files")
    parser.add_argument("--engine", choices=["lualatex", "xelatex"], help="Preferred LaTeX engine")
    parser.add_argument("--passes", type=int, default=1, help="Number of compile passes, default 1")
    args = parser.parse_args()

    tex_path = Path(args.input).resolve()
    if not tex_path.is_file():
        print(f"ERROR: input file not found: {tex_path}", file=sys.stderr)
        return 2
    if tex_path.suffix.lower() != ".tex":
        print(f"ERROR: input must be a .tex file: {tex_path}", file=sys.stderr)
        return 2

    engine = choose_engine(args.engine)
    if not engine:
        requested = args.engine or "lualatex/xelatex"
        print(f"ERROR: no LaTeX engine found ({requested}). Install LaTeX or skip PDF compile.", file=sys.stderr)
        return 3

    output_dir = Path(args.output_dir).resolve() if args.output_dir else tex_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        engine,
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={output_dir}",
        str(tex_path),
    ]

    for run in range(max(args.passes, 1)):
        result = subprocess.run(
            command,
            cwd=tex_path.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            print(f"ERROR: {engine} failed on pass {run + 1}.", file=sys.stderr)
            tail = "\n".join((result.stdout or "").splitlines()[-40:])
            if tail:
                print(tail, file=sys.stderr)
            return result.returncode or 1

    pdf_path = output_dir / f"{tex_path.stem}.pdf"
    if not pdf_path.is_file():
        print(f"ERROR: compile finished but PDF was not created: {pdf_path}", file=sys.stderr)
        return 1

    print(f"OK: created {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
