---
name: job-rank
description: Batch-rank scraped or pasted jobs against the candidate profile, using triage scoring, deal-breaker vetoes, deadline handling, and additive seen-jobs state updates.
---

# Job Rank

Use this skill to rank jobs in `job_scraper/results/`, `job_scraper/seen_jobs.json`, or a pasted list.

Ranking is triage, not a final application evaluation. `job-apply` must re-evaluate any selected job in depth before drafting.

## Arguments and Modes

Support these natural-language equivalents:

- no filter: rank jobs with status `new`
- focus area: rank jobs matching a role, title, skill, or stored note
- all: re-rank every non-applied job
- top N: limit shortlist size

## Step 1: Load State

1. Read `job_scraper/seen_jobs.json`. If it is missing, create `{"seen": {}}` and report that there are no jobs yet.
2. Read every JSON result file under `job_scraper/results/`.
3. Read `job_search_tracker.csv`; build an exclusion set from company+role and URLs already applied to or consciously tracked.
4. Read once:
   - `profile/01-candidate-profile.md`
   - `profile/02-behavioral-profile.md`
   - `profile/04-job-evaluation.md`
5. Select candidates:
   - default: status `new`
   - all mode: all non-applied, non-expired jobs
   - focus mode: matching title/company/source/notes
6. If no candidates remain, say so and suggest `job-scrape`.

## Step 2: Fetch and Score

Fetch full posting content when URLs are available and access is permitted.

Rules:

- Never rank from title alone when full posting text is required for the score.
- If a URL is dead, blocked, or expired, mark the job `expired` or `unfetchable`.
- Do not do company research; that belongs to `job-apply`.
- Do not run salary lookup unless salary is already in the posting or local salary data is explicitly available.
- Use subagents only for bounded batches, around five jobs per batch, and pass the scoring rubric inline.

For each job, score 0-100:

- skills match
- experience match
- education/credential match
- behavioral/work-style fit
- location/remote fit
- language fit
- salary fit if available
- career alignment
- deal-breakers

Also record:

- deadline
- location status: PASS / FLAG / FAIL
- strengths, 1-3 bullets
- gaps, 1-3 honest bullets
- suggested action: apply / maybe / skip

## Step 3: Aggregate

Use the weighting in `profile/04-job-evaluation.md` when present. If no explicit weighting exists, use:

- skills: 30%
- experience: 25%
- behavioral/work style: 15%
- career alignment: 20%
- education/language/salary/location combined: 10%

Apply vetoes:

- deal-breaker FAIL excludes the job regardless of score
- location FAIL excludes unless the user explicitly allows relocation
- expired deadline marks expired

Verdict bands:

- 75-100: strong fit
- 60-74: good fit
- 45-59: moderate fit
- 30-44: weak fit
- below 30: poor fit

Deadline urgency:

- deadline within 7 days gets an urgency note
- past deadline becomes expired

## Step 4: Update State

Update `job_scraper/seen_jobs.json` additively. Do not restructure existing records.

Add fields:

- `status`: `ranked`, `expired`, or `unfetchable`
- `rank_score`
- `rank_verdict`
- `rank_date`
- `rank_strengths`
- `rank_gaps`
- `suggested_action`

Do not modify `job_search_tracker.csv`; ranking is not applying.

Save a dated report under:

`job_scraper/results/ranking-YYYY-MM-DD.md`

## Step 5: Present Shortlist

Output:

```text
Job Ranking - YYYY-MM-DD

Ranked <N> postings (<X> apply, <Y> maybe, <Z> skip, <E> expired/unfetchable).
```

Include:

- shortlist table
- why the top jobs ranked highest
- below-threshold table
- excluded/expired/unfetchable list
- note that triage scores come from posting text and profile only
- next action: pick job number(s) for `job-apply`

Every claim must trace to fetched posting text or profile evidence.
