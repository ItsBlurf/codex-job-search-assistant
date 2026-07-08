---
name: record-outcome
description: Record application progress or final outcomes, update the tracker, archive submitted materials, and preserve calibration notes for future profile updates.
---

# Record Outcome

Use this skill when the user reports progress or a result after applying.

## Step 1: Load and Identify

1. Read `job_search_tracker.csv`.
2. If missing, create it with:

```text
date,company,sector,role,role_type,channel,status,contact_person,fit_rating,notes,cv_file,cover_letter_file,source
```

3. Match by company and role when provided.
4. If several rows match, list them and ask which one.
5. If none match, collect minimum facts:
   - company
   - role
   - date applied
   - channel/source
   - current status

## Step 2: Classify Outcome

Progress statuses:

- applied
- interview
- offer
- in_progress

Final statuses:

- hired
- rejected
- no_response
- withdrawn
- offer_declined
- interview_only

Ask for:

- dates for stages reached
- feedback, as close to verbatim as possible
- what the company seemed to value
- what the user would change next time

Do not impose a no-response cutoff; let the user decide.

## Step 3: Archive Materials

Archive folder:

`documents/applications/<company>-<role>-<date>/`

Copy, never move:

- submitted CV
- submitted cover letter
- job posting
- notes

Rules:

- Existing archived submitted files are not overwritten.
- Dead posting URLs get a stub or user-pasted text, not reconstruction.
- Private archive contents remain ignored by git.

## Step 4: Write Outcome

Create or update `outcome.md`:

```markdown
# Outcome: <Company> - <Role>

**Status:** in_progress | hired | offer_declined | rejected | no_response | interview_only

**Date resolved:** YYYY-MM-DD

## Interview stages reached
- [x] Phone screen (YYYY-MM-DD)
- [ ] Technical interview
- [ ] Case interview
- [ ] Final round
- [ ] Offer received

## Notes
- YYYY-MM-DD: <note>
```

Append notes. Do not rewrite history.

## Step 5: Update Tracker

Update the matched row status and append a dated note. Do not reorder columns or unrelated rows.

## Step 6: Calibration Handoff

Count resolved outcomes. If there are 3+ resolved applications, or 2+ with the same pattern, suggest running `job-setup` to fold outcomes into:

- `profile/04-job-evaluation.md`
- `profile/07-interview-prep.md`
- `profile/03-writing-style.md`

This skill records data; `job-setup` interprets patterns.

## Final Report

Report:

- tracker row changed
- archive files created/copied/skipped
- new status
- notes recorded
- calibration suggestion if triggered
