---
name: job-upskill
description: Analyze target jobs or tracked applications against the candidate profile to identify recurring gaps and produce a prioritized, source-aware learning plan.
---

# Job Upskill

Use this skill to find repeated skill gaps and produce a practical learning plan.

## Modes

- Aggregate: analyze `job_search_tracker.csv`, `job_scraper/results/`, and `job_scraper/seen_jobs.json`.
- Targeted: analyze one pasted posting or URL.

## Step 1: Load Data

Read:

- `profile/01-candidate-profile.md`
- `profile/04-job-evaluation.md`
- target job posting(s)
- previous `upskill/report-*.md` if present

In targeted URL mode, fetch the posting. If fetching fails, ask for pasted text.

## Step 2: Hard Skill Diff

Extract from each job:

- required skills
- preferred skills
- tools/platforms
- domain knowledge
- credentials/certifications
- language requirements

Compare generously against the profile. If the profile proves a skill under a synonym, do not count it as a gap.

Aggregate gaps by:

- frequency
- required vs preferred
- importance to target roles
- fit-score weight when tracker data includes fit ratings

## Step 3: Synthesis Gaps

Identify gaps not captured by keyword diff:

- domain context
- tooling/process maturity
- communication/leadership expectations
- credentials
- portfolio/project evidence gaps

Mark each as:

- hard
- domain
- tooling
- credential
- language
- soft/work-style
- evidence gap

## Step 4: Heatmap

Build a table:

| Priority | Skill / Area | Type | Evidence | Source |
|---|---|---|---|---|

Priority:

- Critical: repeated required gap or deal-breaker for target roles
- High: common preferred gap or important tooling/domain gap
- Medium: useful but not blocking
- Low: one-off nice-to-have

## Step 5: Learning Plan

For Critical and High gaps, produce:

- 2-3 resources when web access is available
- official docs for tools where appropriate
- hands-on project suggestion
- what to skip based on existing profile
- estimated time to working proficiency

If web access is unavailable or sources cannot be verified, mark recommendations as unverified.

Do not invent course names, URLs, authors, or rankings.

## Step 6: Study Order

Order by:

1. dependencies
2. Critical before High before Medium
3. quick wins when useful
4. domain/soft skills alongside practical projects

## Step 7: Save Report

Save:

- aggregate: `upskill/report-YYYY-MM-DD.md`
- targeted: `upskill/report-YYYY-MM-DD-<company>-<role>.md`

Include:

- mode
- sources analyzed
- gap heatmap
- learning plan
- suggested order
- changes since previous report if available
- unverified recommendations
