# Milestone 2 Grade

**Team 18**

| Category | Score | Max |
|---|---|---|
| Pipeline Functionality | 4 | 6 |
| Parameterization | 4 | 6 |
| Code Quality | 4 | 6 |
| Project Structure | 3 | 3 |
| DESIGN.md | 2 | 3 |
| **Total** | **17** | **24** |

---

## Pipeline Functionality (4/6)

Pipeline runs and produces all three required outputs (summary.csv, detail.parquet, chart.html). Holdout dataset (olist_extended.duckdb) passes cleanly with no hardcoded assumptions. However, `--db-path` is a required argument — running `uv run wvu-ieng-331-m2-18` without arguments fails with an argparse error rather than defaulting to `data/olist.duckdb`. Also, the ABC classification SQL (`abc_classification.sql`) does not actually implement ABC tiering (no A/B/C column computed); it only returns `(product_id, total_revenue)` ordered by revenue — the analysis is incomplete.

## Parameterization (4/6)

Three optional parameters are declared (`--seller-id`, `--start-date`, `--end-date`). `--seller-id` genuinely affects output by running a separate seller scorecard query. However, `--start-date` and `--end-date` are parsed but never passed into any query or used to filter results — they have no effect on pipeline output. README even acknowledges "may not fully affect all queries." No input validation (e.g., date format checking, seller-id existence check) is implemented beyond argparse defaults.

## Code Quality (4/6)

Strengths: loguru used consistently, pathlib used for file paths, docstrings present on all public functions in queries.py and validation.py, SQL external files loaded via pathlib. Weaknesses: no type hints on function signatures (no parameter types or return types annotated), broad `except Exception as e` in validation rather than specific exceptions, altair import is placed inside the function body rather than at module top, and `__init__.py` retains a leftover `print("Hello from wvu-ieng-331-m2-18!")` stub from the project template that conflicts with the actual `main()` entry point in pipeline.py.

## Project Structure (3/3)

Proper `src/` layout, `pyproject.toml` with `[project.scripts]`, external SQL files in `sql/`, README.md, DESIGN.md, `.gitignore`, `.python-version`. Well organized.

## DESIGN.md (2/3)

Five substantive sections: Parameter Flow, SQL Parameterization, Validation Logic, Error Handling, Scaling & Adaptation. Each section includes real code snippets and references to actual files. However, the document does not acknowledge that `--start-date` and `--end-date` have no actual effect on query results, and the ABC classification is described as doing tiering that the SQL does not implement. Generic scaling advice without specific DuckDB or Polars considerations.
