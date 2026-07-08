---
name: add-job-portal
description: Add a modular public job-portal adapter after access-rule inspection, endpoint documentation, implementation, and live harmless testing.
---

# Add Job Portal

Use this skill to add support for another public job board.

## Rules

- Inspect before coding.
- Check public access, robots.txt, and practical limitations.
- Do not bypass anti-bot protections, login walls, CAPTCHAs, or paywalls.
- Prefer official APIs or public JSON endpoints.
- Keep test volume low.
- Document personal-use limitations clearly.

## Step 1: Collect Basics

Collect:

- portal URL
- market/country/region
- language
- realistic test query
- desired skill name, ending in `-search`

## Step 2: Investigate

Fetch and inspect:

- search page
- one search-result response
- one detail page
- `robots.txt`
- visible terms/access restrictions

Record:

- endpoints
- query parameters
- pagination
- location parameter behavior
- result fields
- detail fields
- deadline/apply-link location
- rate-limit or blocking behavior

If the portal is auth-walled or restrictive, stop or document a personal-use-only warning if the user still proceeds within allowed boundaries.

## Step 3: Scaffold

Create:

```text
.agents/skills/<name>/
  SKILL.md
  url-reference.md
  cli/
    package.json
    tsconfig.json
    README.md
    src/cli.ts
    src/helpers.ts
    src/commands/search.ts
    src/commands/detail.ts
    tests/helpers.ts
```

Use existing portal skills as references, especially `linkedin-search` for zero-runtime-dependency structure.

## Adapter Contract

Commands:

- `search`
- `detail <id|url>`

Search flags:

- `--query` / `-q`
- `--location` / `-l` if supported
- `--jobage <days>` if supported
- `--page <n>`
- `--limit <n>`
- `--format json|table|plain`

JSON shape:

```json
{
  "meta": { "count": 0, "page": 1 },
  "results": [
    {
      "id": "...",
      "title": "...",
      "company": "...",
      "location": "...",
      "date": "...",
      "url": "..."
    }
  ]
}
```

Errors go to stderr as JSON and exit nonzero.

## Step 4: Test

When Bun is available:

```bash
cd .agents/skills/<name>/cli
bun install
bun run typecheck
bun run src/cli.ts search -q "<query>" --limit 5 --format table
bun run src/cli.ts detail <id> --format plain
bun run test
```

If testing fails, fix parsers or document limitations. Do not claim a portal works without a live harmless test.

## Step 5: Register

Update `job_scraper/search-queries.md` only when the user wants the portal included by default.

## Final Report

Report:

- files created
- access/terms notes
- live test result
- limitations
- example command
