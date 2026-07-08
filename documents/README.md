# Documents Folder

This folder holds private career documents. The `job-setup` skill reads these files and uses them to populate `profile/`. It is safe to re-run as you add documents: Codex should merge intelligently and ask before changing conflicting information.

## Folder Structure

```text
documents/
  cv/
  linkedin/
  diplomas/
  references/
  applications/
    <company>-<role>-<date>/
      job_posting.md
      cover_letter.tex
      cv.tex
      outcome.md
```

## cv/

Store your most complete master CV here.

Supported formats: `.pdf`, `.tex`, `.md`, `.txt`

`job-setup` extracts work experience, education, skills, awards, publications, and contact information.

## linkedin/

Store a LinkedIn profile export or copied profile text here.

`job-setup` extracts work history, education, skills, certifications, volunteer work, publications, summary text, and recommendations.

## diplomas/

Store degree certificates, transcripts, and qualification records here.

`job-setup` uses these to verify degree names, institutions, graduation dates, grades, and distinctions.

## references/

Store reference letters here.

`job-setup` extracts referee details, direct quotes, and competency language. Inferred behavioral signals must be marked as inferred.

## applications/

Each subfolder is one application archive. `job-apply` and `record-outcome` can create and update these folders.

`job_posting.md` stores the posting text.

`cover_letter.tex` stores the submitted cover letter.

`cv.tex` stores the submitted CV.

`outcome.md` records what happened:

```markdown
# Outcome: <Company> - <Role>

**Status:** in_progress | hired | offer_declined | rejected | no_response | interview_only

**Date resolved:** YYYY-MM-DD

## Interview stages reached
- [ ] Phone screen
- [ ] Technical interview
- [ ] Case interview
- [ ] Final round
- [ ] Offer received

## Notes
What happened? What feedback did you receive?
What would you do differently?
```

`job-setup` can later use resolved outcomes to calibrate the evaluation profile.

## Privacy

Everything under the private document subfolders is ignored by git except `.gitkeep` placeholders and this README. Do not commit diplomas, passports, CVs, reference letters, private notes, or generated application PDFs.
