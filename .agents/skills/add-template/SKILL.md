---
name: add-template
description: Register a custom CV or cover-letter template with metadata, compile verification, activation rules, and rollback to stock templates.
---

# Add Template

Use this skill to add, list, activate, or deactivate CV and cover-letter templates.

## Modes

- list: show registered templates from `templates/**/TEMPLATE.md`
- use `<name>`: activate a template
- use default: remove active custom template
- register: add a new template

## Step 1: Inspect Source

Accept:

- `.tex` file
- directory with `.tex`, `.cls`, `.sty`, fonts, and images
- pasted LaTeX

Read all referenced local assets. If a required class/font is missing, stop and ask for it.

## Step 2: Infer Metadata

Infer before asking:

- type: CV or cover letter
- compile engine
- document class
- font usage
- page limit
- geometry/margins
- required fields
- style rules
- known pitfalls

Engine rules:

- `fontspec` or local font files require `xelatex` or `lualatex`
- stock cover-letter template uses `xelatex`
- stock CV template uses `lualatex`
- do not choose `pdflatex` for templates requiring modern font handling

## Step 3: Store Template

Store under:

- `templates/cv/<name>/`
- `templates/cover_letters/<name>/`

Write:

- `template.tex`
- copied `.cls`/`.sty` assets
- copied `fonts/`
- `TEMPLATE.md`

Replace personal data with placeholders. Escape placeholder syntax so the template compiles.

Manifest format:

```markdown
# Template: <name>

- **Type:** CV | Cover letter
- **Engine:** lualatex | xelatex | pdflatex
- **Page limit:** <N>
- **Fonts:** <summary>
- **Required fields:** <fields>
- **Class/packages:** <summary>

## Compile command

...

## Style rules

...

## Known pitfalls

...
```

## Step 4: Mandatory Compile Test

If LaTeX exists:

1. Create `_compile_test.tex` from the template.
2. Fill placeholders with realistic dummy data.
3. Compile with `python tools/compile_latex.py`.
4. Inspect output for page count, font loading, obvious overflow, and missing text.
5. Run `tools/ats_check.py` for CV templates when `pdftotext` exists.
6. Delete scratch files and build artifacts after success.

If LaTeX is missing, do not mark the template verified. Store it as unverified.

## Step 5: Activate

Activation is a managed block in:

- `profile/05-cv-rules.md` for CVs
- `profile/06-cover-letter-rules.md` for cover letters

Use exactly one block:

```markdown
<!-- BEGIN ACTIVE-TEMPLATE -->
...
<!-- END ACTIVE-TEMPLATE -->
```

The block must include:

- template path
- manifest path
- engine
- page limit
- required assets
- output-location guidance

`use default` removes the managed block only.

## Final Report

Report:

- template name/type
- files stored
- compile result
- ATS result if applicable
- activation status
- limitations
