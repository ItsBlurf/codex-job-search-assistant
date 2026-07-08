<p align="center">
  <img src="assets/codex-job-search-icon.svg" alt="Codex Job Search Assistant" width="128">
</p>

# Codex Job Search Assistant

A Codex-native job application workspace for building a grounded candidate profile, finding and ranking jobs, producing tailored CVs and cover letters, compiling PDFs, checking ATS text extraction, and tracking application outcomes.

This project is adapted from the [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search) project. The original is built for Claude Code slash commands. This version is built for OpenAI Codex with `AGENTS.md`, Codex skills, explicit validation tools, and clear fallback behavior.

## What It Does

- Builds a candidate profile from CVs, LinkedIn exports, diplomas, references, notes, and past applications.
- Keeps facts grounded in source documents and marks uncertainty instead of inventing.
- Searches supported job portals and stores normalized results.
- Ranks jobs against the profile with honest strengths, gaps, deal-breakers, and apply/maybe/skip recommendations.
- Generates tailored LaTeX CVs and cover letters for specific jobs.
- Compiles PDFs with LaTeX when available.
- Runs ATS text-layer checks with `pdftotext` when available.
- Tracks applications and outcomes in `job_search_tracker.csv`.
- Supports adding new portals and custom templates.

## Quick Start

Clone the repo, open it in Codex, and run:

```bash
python tools/setup_check.py
python tests/smoke/validate_repo.py --full
```

Then add your real career documents:

```text
documents/cv/
documents/linkedin/
documents/diplomas/
documents/references/
documents/applications/
```

In Codex, send this first prompt:

```text
Use the job-setup skill to build my profile from the documents folder. Do not invent anything. Ask only for important missing information.
```

After setup, send:

```text
Use the profile-expand skill to find source-traceable skills and competencies I may have missed. Add nothing unsupported.
```

## Exact Codex Prompts

Build or update the profile:

```text
Use the job-setup skill to build my profile from the documents folder. Do not invent anything. Ask only for important missing information.
```

Apply to a job:

```text
Use the job-apply skill for this job: <paste URL or job description>. Evaluate the fit first, then generate a tailored CV and cover letter.
```

Search for jobs:

```text
Use the job-scrape skill to search for <role> jobs in <location>. Save results and deduplicate against seen_jobs.json.
```

Rank saved jobs:

```text
Use the job-rank skill to rank the jobs in job_scraper/results against my profile.
```

Record an outcome:

```text
Use the record-outcome skill to record the outcome for <company> / <role>.
```

Find recurring skill gaps:

```text
Use the job-upskill skill to analyze my tracked jobs and produce a prioritized learning plan.
```

Add a portal:

```text
Use the add-job-portal skill to add support for <job board URL>. Respect access limits and do not bypass anti-bot protections.
```

Add a template:

```text
Use the add-template skill to register this CV template: <path>. Test compile it before activation.
```

## Repository Structure

```text
codex-job-search-assistant/
  AGENTS.md
  README.md
  SETUP.md
  QUALITY_COMPARISON.md
  assets/
  .agents/skills/
  profile/
  documents/
  cv/
  cover_letters/
  templates/
  job_scraper/
  tools/
  tests/smoke/
  job_search_tracker.csv
```

## Main Workflows

### Profile Setup

The `job-setup` skill has three modes:

- documents-folder import
- single-CV import
- interview mode

It reads existing `profile/` files before writing, cross-checks dates/titles/education, labels inferred information, and asks before resolving factual conflicts.

### Profile Expansion

The `profile-expand` skill searches your own documents and public profile links for source-traceable competencies that may be missing from the profile. It is additive only.

### Job Application

The `job-apply` skill runs a serious drafter-reviewer workflow:

1. parse and save the job posting
2. evaluate fit
3. draft CV and cover letter from profile evidence
4. review grounding, tone, fit, and keywords
5. revise
6. compile PDFs
7. run ATS extraction
8. update the tracker
9. report passed, failed, and skipped checks

### Job Search and Ranking

The `job-scrape` skill searches supported sources and saves results under `job_scraper/results/`.

The `job-rank` skill scores jobs from posting text and profile evidence only. Ranking is triage; `job-apply` re-evaluates any job before drafting.

### Outcomes

The `record-outcome` skill updates `job_search_tracker.csv`, archives submitted materials, and stores notes for future calibration.

## Tools

Required:

- Python 3.10+
- Git

Optional but recommended:

- `lualatex` and `xelatex` for PDF compilation
- Poppler `pdftotext` for ATS extraction
- Bun for portal CLI skills
- Node.js for some portal development workflows

Check local readiness:

```bash
python tools/setup_check.py
```

Run repository smoke checks:

```bash
python tests/smoke/validate_repo.py
```

Run full local checks, including LaTeX and portal CLI smoke checks when tools are installed:

```bash
python tests/smoke/validate_repo.py --full
```

Compile examples manually:

```bash
python tools/compile_latex.py cv/main_example.tex --engine lualatex
python tools/compile_latex.py cover_letters/example_cover_letter.tex --engine xelatex
python tools/ats_check.py cv/main_example.pdf
```

## Privacy and Security

Private folders and generated outputs are ignored by git:

- `documents/cv/*`
- `documents/linkedin/*`
- `documents/diplomas/*`
- `documents/references/*`
- `documents/applications/**`
- generated PDFs
- scraper result batches
- `salary_data.json`
- `.env`

Do not commit CVs, diplomas, passports, references, private notes, generated applications, salary data, or secrets.

## Troubleshooting

- Missing LaTeX: `.tex` files can still be generated; PDFs cannot be claimed ready.
- Missing `pdftotext`: ATS extraction is skipped and reported.
- Missing Bun: portal CLIs are skipped; pasted postings and web search remain available.
- Dead job URL: paste the full job description into Codex.
- Missing salary data: salary benchmarking is optional and skipped.

See [SETUP.md](SETUP.md) for Windows, macOS, Linux, and Windows LTSC setup notes.

## Quality Standard

See [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for the original-to-Codex workflow comparison and the validation bar used for this repo.

## License

MIT. This project preserves attribution to [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search).
