---
name: job-scrape
description: Search job portals using configured queries and portal adapters, deduplicate results, save normalized job records, and fall back cleanly when scraping is blocked.
---

# Job Scrape

Use this skill to find jobs and save results for ranking.

## Rules

- Respect legal and access limits.
- Do not bypass anti-bot protections, authentication, CAPTCHAs, rate limits, or paywalls.
- Prefer public pages, official APIs, and the repo's portal adapters.
- If a portal blocks access, explain clearly and support pasted job descriptions as fallback.
- Never fabricate job postings.

## Step 1: Load State

Read:

- `job_scraper/seen_jobs.json` or create `{"seen": {}}`
- `job_search_tracker.csv`
- `job_scraper/search-queries.md`
- `profile/01-candidate-profile.md`
- `profile/04-job-evaluation.md`

Build exclusion sets from:

- seen URL/id
- company+title
- already-applied tracker rows

## Step 2: Choose Search Strategy

Use the user's focus if provided. Otherwise use the highest-priority configured queries.

Strategy order:

1. Portal CLI skills under `.agents/skills/*-search` when Bun is available.
2. Web search with site-specific queries from `job_scraper/search-queries.md`.
3. User-pasted job descriptions.

For portal CLIs, follow each skill's `SKILL.md` and CLI README. Keep volume low.

## Step 3: Fetch and Normalize

For each result, capture:

- id
- title
- company
- location
- date
- deadline
- url
- source
- short description or key requirements
- first_seen
- status: `new`, `skipped`, `ranked`, `expired`, or `unfetchable`

Skip:

- duplicates
- closed/expired jobs
- jobs outside hard location constraints
- auth-walled pages

Do a quick fit signal only:

- high: direct match to core profile
- medium: adjacent match
- low: likely large gaps

Full scoring belongs to `job-rank`.

## Step 4: Save

Save batch results:

`job_scraper/results/jobs-YYYY-MM-DD.json`

Update `job_scraper/seen_jobs.json` additively:

```json
{
  "seen": {
    "<stable-key>": {
      "id": "...",
      "title": "...",
      "company": "...",
      "location": "...",
      "url": "...",
      "source": "...",
      "first_seen": "YYYY-MM-DD",
      "fit": "high|medium|low",
      "status": "new"
    }
  }
}
```

## Step 5: Present

Report:

- searches run
- portals used
- portals skipped and why
- new jobs found
- duplicates skipped
- failed fetches
- high/medium/low quick-fit counts
- path to saved results
- recommendation to run `job-rank` when there are several jobs

If the user selects one job, hand off to `job-apply`; do not treat scrape quick-fit as the final evaluation.
