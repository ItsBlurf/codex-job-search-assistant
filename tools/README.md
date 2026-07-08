# Tools

- `setup_check.py` reports local readiness.
- `compile_latex.py` compiles `.tex` files with `lualatex` or `xelatex`.
- `ats_check.py` extracts PDF text with `pdftotext` and performs basic ATS readability checks.
- `salary_lookup.py` is optional and only works when salary data is available.
- `convert_salary_excel.py` converts external salary data to JSON when needed.

All tools should fail gracefully and avoid tracebacks for normal missing-tool cases.
