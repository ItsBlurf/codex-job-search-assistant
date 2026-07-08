# Quality Comparison: Original vs Codex Version

This file records the parity check against the original `MadsLorentzen/ai-job-search` project and the extra quality bar for this Codex-native version.

## Summary

The original project is a Claude Code workflow repo built around slash commands, `CLAUDE.md`, `.claude/skills/`, and portal CLI skills under `.agents/skills/`.

The Codex version keeps the project model but replaces command mechanics with Codex skills, `AGENTS.md`, `profile/`, explicit setup checks, and repo-local helper tools.

## What the Original Has

- Profile onboarding from documents, single CV, or interview.
- Read-before-write profile merging.
- Conflict handling for dates, titles, and education.
- Drafter-reviewer job application workflow.
- Mandatory LaTeX compile and visual/PDF checks.
- ATS text-layer extraction with `pdftotext`.
- Relevance-weighted CV and cover-letter trimming.
- Job scraping and deduplication.
- Batch ranking of scraped jobs.
- Outcome recording and application archive.
- Competency expansion from documents and public links.
- Upskill gap analysis.
- Custom template registration.
- Job portal adapter generation.
- Salary lookup with user-provided data.
- Privacy-focused document folders.

## Claude-Specific Parts

- `CLAUDE.md` as the main instruction file.
- `.claude/commands/*.md` slash commands.
- `.claude/skills/*` skill references.
- Claude tool names and command invocation language.
- Claude-specific reviewer/subagent wording.
- Claude settings file.

## Codex Mapping

| Original | Codex Version |
|---|---|
| `CLAUDE.md` | `AGENTS.md` plus candidate facts in `profile/` |
| `/setup` | `.agents/skills/job-setup/SKILL.md` |
| `/apply` | `.agents/skills/job-apply/SKILL.md` |
| `/rank` | `.agents/skills/job-rank/SKILL.md` |
| `/scrape` | `.agents/skills/job-scrape/SKILL.md` |
| `/outcome` | `.agents/skills/record-outcome/SKILL.md` |
| `/expand` | `.agents/skills/profile-expand/SKILL.md` |
| `/upskill` | `.agents/skills/job-upskill/SKILL.md` |
| `/add-template` | `.agents/skills/add-template/SKILL.md` |
| `/add-portal` | `.agents/skills/add-job-portal/SKILL.md` |
| `.claude/skills/job-application-assistant/*.md` | `profile/*.md` |
| `.claude/skills/job-scraper/search-queries.md` | `job_scraper/search-queries.md` |
| portal CLI skills | retained under `.agents/skills/*-search` |

## Improvements in the Codex Version

- `tools/setup_check.py` gives a readable readiness report.
- `tools/compile_latex.py` provides a consistent compile wrapper.
- `tools/ats_check.py` provides a consistent ATS extraction wrapper.
- Windows LTSC setup path is documented and tested with Scoop/MiKTeX.
- Poppler and Bun are verified in setup checks.
- `AGENTS.md` separates repo rules from private candidate facts.
- `.gitignore` more explicitly protects private documents and generated PDFs.
- `profile-expand` preserves original expansion behavior in Codex-native form.
- Skills now include detailed operational steps rather than only short summaries.

## Remaining Differences

- The original slash-command UX is intentionally not preserved. Codex uses natural-language skill invocation.
- The original Claude-specific settings and agent definitions are intentionally omitted.
- Market-specific portal CLIs are retained, but adding a new portal still depends on live website access and each site's rules.
- PDF visual inspection still depends on Codex being able to inspect rendered PDFs in the active environment; compile and ATS text checks are automated.

## Quality Bar for Future Changes

Before considering this repo ready after workflow changes:

1. `python tools/setup_check.py` passes.
2. Every required skill has YAML front matter with `name` and `description`.
3. No required workflow depends on `.claude/commands`.
4. `cv/main_example.tex` compiles with `lualatex`.
5. `cover_letters/example_cover_letter.tex` compiles with `xelatex`.
6. `python tools/ats_check.py cv/main_example.pdf` passes.
7. Private document folders and generated PDFs remain ignored by git.
8. README and SETUP match actual paths and tools.
9. New workflows preserve the no-fabrication rule.
