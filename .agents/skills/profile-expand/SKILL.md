---
name: profile-expand
description: Additively enrich the candidate profile by discovering source-traceable competencies from documents and public profile links without overwriting existing facts.
---

# Profile Expand

Use this skill when the user wants to surface competencies hidden in documents, coursework, references, GitHub, portfolio pages, publications, or other public profile links.

This is additive only. It never deletes or rewrites existing profile content.

## Step 1: Read Existing Profile

Read:

- `profile/01-candidate-profile.md`
- `profile/02-behavioral-profile.md`

Build a set of skills, domains, methods, tools, projects, and behavioral signals already present.

## Step 2: Discover Sources

Scan:

- `documents/cv/`
- `documents/linkedin/`
- `documents/diplomas/`
- `documents/references/`
- `documents/applications/`
- public URLs already present in the profile, such as GitHub, portfolio, Kaggle, Google Scholar, ResearchGate, personal site, or publication links

Extract experience items:

- courses/modules
- certifications
- project descriptions
- repo names and README technologies
- thesis and transcript topics
- reference-letter competency language
- tools/frameworks/methods
- datasets/domains

## Step 3: Enrich Competencies

For each item:

- directly record named tools and frameworks
- infer reasonable competencies from the work described
- use web lookup for named courses/certifications/public repos when available
- mark unverified inferences when web lookup is unavailable

Do not turn weak evidence into a strong claim. For example, "course exposed candidate to X" is not the same as "professional experience in X."

## Step 4: Deduplicate and Group

Group new signals:

- Technical Skills - Primary
- Technical Skills - Secondary
- Domain Knowledge
- Methods and Practices
- Tools and Platforms
- Portfolio Evidence
- Soft / Behavioral
- Interview STAR Candidates

Every addition needs a source annotation.

## Step 5: Confirm and Write

Present grouped additions before writing unless the user explicitly requested autonomous changes.

Write additions to:

- `profile/01-candidate-profile.md`
- `profile/02-behavioral-profile.md`
- `profile/07-interview-prep.md`

Use targeted edits. Do not rewrite entire files.

## Final Report

Report:

- sources scanned
- additions made
- sources skipped
- unverified inferences
- items needing manual review
