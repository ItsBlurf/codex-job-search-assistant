# Custom Templates

This folder stores user-registered LaTeX CV and cover-letter templates. The repo works with the stock templates in `cv/` and `cover_letters/`; add custom templates only when needed.

## Layout

```text
templates/
  cv/
    <template-name>/
      template.tex
      TEMPLATE.md
      fonts/
  cover_letters/
    <template-name>/
      template.tex
      TEMPLATE.md
      fonts/
```

Use the `add-template` skill to register a template. It should document compile engine, fonts, required fields, style rules, page limits, and known pitfalls. It should test compilation when LaTeX is available.

Templates should use `[PLACEHOLDER]` tokens instead of personal data so they are safe to commit.
