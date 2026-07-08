# Setup

This repo is usable with only Python and Codex. LaTeX, Poppler, and Bun improve the workflow but are optional.

## Check Readiness

Run from the repository root:

```bash
python tools/setup_check.py
```

The check reports Python, expected folders, important commands, optional commands, and a concise readiness summary.

## Python

Python 3.10+ is required. No Python packages are required for the baseline checks.

If you later add dependencies, prefer a local virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## LaTeX

Optional but recommended for PDFs:

- `lualatex` for CVs
- `xelatex` for cover letters

Windows:

```powershell
winget install MiKTeX.MiKTeX
```

Windows LTSC or systems without Microsoft Store / App Installer:

```powershell
scoop install miktex
```

If Scoop's MiKTeX wrapper fails after the official installer has already expanded files, verify the engines directly:

```powershell
lualatex --version
xelatex --version
```

macOS:

```bash
brew install --cask mactex
```

Linux:

```bash
sudo apt install texlive-luatex texlive-xetex texlive-fonts-extra
```

For Fedora:

```bash
sudo dnf install texlive-scheme-medium
```

## Poppler / pdftotext

Optional for ATS checks.

Windows:

```powershell
winget install oschwartz10612.Poppler
```

macOS:

```bash
brew install poppler
```

Linux:

```bash
sudo apt install poppler-utils
```

## Bun and Node

Bun is only needed for the TypeScript job portal CLI skills. Do not install it unless you plan to run or develop those adapters.

Windows:

```powershell
winget install Oven-sh.Bun
```

macOS:

```bash
brew install oven-sh/bun/bun
```

Linux:

```bash
curl -fsSL https://bun.sh/install | bash
```

Do not run untrusted install scripts for random tools. Bun's script is official, but a package manager is preferred when available.

## What Codex Can Install

With full filesystem access and network enabled, Codex can safely:

- create a local Python virtual environment
- install Python packages into that virtual environment when a workflow needs them
- run `bun install` inside a specific portal CLI when Bun is already installed
- use `winget`, Homebrew, or distro package managers for standard tools when they do not require an interactive admin prompt

Codex should document the exact manual command when administrator/root permission is required or an installer is too heavy for the current workflow.

## Ready State

The repo is ready when:

- `python tools/setup_check.py` runs without a traceback
- `AGENTS.md` exists
- each required workflow under `.agents/skills/` has a `SKILL.md`
- `job_search_tracker.csv` exists
- `job_scraper/seen_jobs.json` is valid JSON
- optional missing tools are reported clearly
