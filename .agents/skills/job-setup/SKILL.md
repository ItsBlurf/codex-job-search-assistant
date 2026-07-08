---
name: job-setup
description: Build or update the candidate profile from the documents folder, a single CV, or interview answers with read-before-write merging, conflict handling, search configuration, and completeness reporting.
---

# Job Setup

Use this skill when the user wants to create, repair, or update the candidate profile.

## Quality Bar

- The profile must be evidence-grounded.
- Existing useful information must be preserved.
- Conflicts must be surfaced before writing.
- Inferred information must be labeled.
- The user should not need to understand Markdown or LaTeX.
- Ask only important missing questions.

## Step 0: Pick Setup Path

Inventory:

- `documents/cv/`
- `documents/linkedin/`
- `documents/diplomas/`
- `documents/references/`
- `documents/applications/`

Then choose:

- Path A: documents-folder import when documents exist
- Path B: single-CV import when the user provides one CV
- Path C: interview mode when documents are absent or incomplete
- Section update: when the user asks to update only search, skills, experience, writing style, or another section

If the user says "do everything," use Path A when documents exist; otherwise start interview mode and keep questions concise.

## Step 1: Read Existing Profile

Read all profile files before extracting anything:

- `profile/01-candidate-profile.md`
- `profile/02-behavioral-profile.md`
- `profile/03-writing-style.md`
- `profile/04-job-evaluation.md`
- `profile/05-cv-rules.md`
- `profile/06-cover-letter-rules.md`
- `profile/07-interview-prep.md`
- `job_scraper/search-queries.md`
- `cv/main_example.tex`

Do not re-read unless a file changed.

## Path A: Documents Folder Import

### A1 Inventory

List files by folder. If all are empty, stop with a short instruction to add documents.

### A2 Extract Facts

Process in this order:

1. `documents/cv/`
2. `documents/linkedin/`
3. `documents/diplomas/`
4. `documents/references/`
5. `documents/applications/`

Extract:

- identity and contact
- education with official degree names
- experience: title, company, dates, location, responsibilities, achievements, tools
- skills with evidence
- languages and proficiency
- certifications
- publications and awards
- references and quotes
- behavioral signals
- writing patterns from past applications
- role targets and outcomes from past applications

### A3 Cross-Reference

Check:

- date mismatches
- title mismatches
- degree/institution spelling mismatches
- employer name variations
- contact differences
- language-level conflicts

If conflicts affect factual accuracy, present them and wait for resolution. Do not guess.

### A4 Build Change Sets

Create two buckets:

- additive changes: new facts that do not conflict
- conflicting changes: different value for an existing fact

Inference rules:

- Behavioral additions from LinkedIn/references must be labeled: `[Inferred from <source>; review before relying on this]`.
- Writing style additions from past cover letters require a repeated pattern, preferably 2+ examples.
- Evaluation calibration from past outcomes must distinguish interviews/offers from rejections/no-response.
- STAR examples from documents should start as stubs unless the source contains enough Situation/Task/Action/Result detail.

### A5 Confirm and Write

For additive changes, summarize grouped by target file and ask before writing unless the user explicitly asked for full autonomous setup.

For conflicts, ask one at a time.

Make targeted edits. Do not rewrite entire files unnecessarily.

## Path B: Single CV Import

1. Read the CV thoroughly.
2. Extract structured facts.
3. Present an extraction summary.
4. Ask only for important gaps:
   - behavioral profile
   - target roles
   - deal-breakers
   - salary baseline if desired
   - location/remote constraints
   - search configuration
5. Populate profile files and CV template from grounded facts.

## Path C: Interview Mode

Ask conversationally in sections:

1. identity/contact
2. education
3. experience
4. technical and domain skills
5. projects/publications/awards
6. behavioral profile
7. career goals and preferences
8. references
9. job-search configuration

For search configuration, collect:

- 3-8 role titles
- 3-5 distinctive skills
- target companies if any
- locations/commute/remote tiers
- portals to use
- adjacent role suggestions the user may not have considered

## Generated/Updated Files

Update as supported by evidence:

- `profile/01-candidate-profile.md`
- `profile/02-behavioral-profile.md`
- `profile/03-writing-style.md`
- `profile/04-job-evaluation.md`
- `profile/05-cv-rules.md`
- `profile/06-cover-letter-rules.md`
- `profile/07-interview-prep.md`
- `job_scraper/search-queries.md`
- `cv/main_example.tex`

Do not place private facts into `AGENTS.md`; it contains repo instructions, not the candidate profile.

## Final Report

Report:

- files changed
- facts added
- conflicts resolved
- uncertain/inferred facts
- important missing information
- profile completeness checklist
- next recommended workflow

Completeness checklist:

- identity/contact
- education
- experience
- skills with evidence
- languages
- certifications
- publications/awards
- references
- writing style
- role targets
- location/remote constraints
- salary baseline if used
- deal-breakers
- CV rules
- cover-letter rules
- interview examples
- search queries
