# System Design: Data Pipeline and Reporting Layer

## Overview

This project extends the Milestone 2 pipeline into a complete data product by adding a reporting layer that delivers insights to non-technical stakeholders.

The system transforms raw data from a DuckDB database into structured outputs and a final self-contained HTML report. The pipeline is fully automated and reproducible, requiring only a single command to regenerate all outputs.

---

## Architecture

The system is organized into modular components:

- **Data Source Layer**
  - DuckDB database (`olist.duckdb`)

- **Validation Layer (`validation.py`)**
  - Ensures required tables exist
  - Prevents execution on invalid datasets

- **Data Access Layer (`queries.py`)**
  - Executes parameterized SQL queries
  - Encapsulates data retrieval logic

- **Pipeline Orchestration (`pipeline.py`)**
  - Coordinates validation, querying, and output generation
  - Produces intermediate outputs (CSV, Parquet, chart)

- **Reporting Layer (`report.py`)**
  - Generates the final HTML report
  - Combines visualizations with narrative explanations

---

## Data Flow

The pipeline executes in the following sequence:

1. Validate database schema
2. Execute SQL queries
3. Generate intermediate outputs:
   - `summary.csv`
   - `detail.parquet`
   - `chart.html`
4. Pass results into reporting module
5. Generate final deliverable:
   - `report.html`

This ensures a fully reproducible workflow from raw data to stakeholder-facing insights.

---

## Design Rationale

## Parameter Flow

Command-line parameters (`--start-date`, `--end-date`, `--seller-id`) are parsed in `pipeline.py` and passed into the query layer.

These parameters are bound to SQL queries using DuckDB parameter substitution, ensuring that filtering is dynamic and safe without modifying SQL logic.

```python
parser.add_argument("--seller-id", default=None)
```
After parsing, all arguments are stored in the args object. For example, args.seller_id holds the value passed by the user.

This value is then passed into the data access layer. In pipeline.py, the function call:
df_seller = get_seller_scorecard(args.db_path, args.seller_id)
sends the parameter into the queries.py module. Inside queries.py, the value is passed as a parameter when executing the SQL query.

This design allows command-line inputs to directly influence the database query results without modifying SQL code, making the pipeline flexible and reusable.

## SQL Parameterization

SQL queries in this project use parameterized placeholders (e.g., `$1`) to safely inject runtime values into database queries without modifying the SQL structure.

For example, a query such as:

```sql
SELECT *
FROM sellers
WHERE seller_id = $1;
```

In queries.py, the SQL file is read using pathlib, and then executed like this:
```python
conn.execute(sql, [seller_id])
```
The value of seller_id is passed safely into the query.

This approach ensures that user-provided values are passed as data rather than being concatenated into the SQL string.

Using parameterized queries provides two key benefits:
- Security: Prevents SQL injection by separating query structure from input values.
- Maintainability: Keeps SQL logic static in .sql files while allowing dynamic filtering at runtime.

All SQL queries are stored in external .sql files rather than embedded in Python code. This separation improves readability and makes query logic easier to update without changing application code.

## Validation Logic

Validation is implemented in the validate_database() function in validation.py.

The main validation step checks that all required tables exist in the database. These include:
- orders  
- order_items  
- customers  
- products  
- sellers  
- geolocation  
- order_payments  
- order_reviews  
- category_translation 

This check is important because all queries depend on these tables. If any are missing, the pipeline would fail during execution.

If any required tables are missing, the function logs a warning and returns False. The pipeline then stops execution to prevent invalid analysis.

The validation also logs a message confirming that the dataset schema is valid and that the pipeline does not rely on fixed row counts or date ranges. This ensures compatibility with the holdout dataset, which may contain more data.

No strict row count thresholds are enforced because the dataset size may change. Instead of failing on different sizes, the pipeline is designed to adapt to varying amounts of data.

## Error Handling

One example of error handling is in validation.py:
try:
    conn = duckdb.connect(db_path)
except Exception as e:
    logger.error(f"Validation failed: {e}")
    
This catches errors related to connecting to the database, such as missing or invalid files. If an error occurs, the pipeline logs the issue and stops safely.

Another example is during query execution in queries.py. If a query fails (for example, due to invalid SQL or missing tables), DuckDB raises an exception that prevents incorrect data from being returned.

Specific exceptions are used instead of a bare except: to avoid hiding errors. A bare except: could catch unrelated issues and make debugging difficult. By handling errors explicitly, the pipeline provides clearer feedback to the user.

## Scaling & Adaptation

If the dataset grew to 10 million orders, the main performance bottleneck would likely be query execution and data conversion, especially when converting large datasets to pandas for visualization. This could slow down the pipeline. To improve performance, I would:
Optimize SQL queries to reduce data size before returning results
Avoid converting large datasets to pandas when possible
Use aggregation in SQL instead of processing large datasets in Python
To add a third output format (such as JSON), I would modify the output section of pipeline.py. After generating the main DataFrame, I would add a new export step such as:
df_abc.write_json("output/data.json")

This would be added alongside the existing CSV and Parquet outputs. Because the pipeline separates data processing from output generation, adding new formats is straightforward.

## Reporting Layer Design

The reporting layer is implemented in `report.py` and is responsible for transforming analytical outputs into a stakeholder-friendly format.

The report is generated as a self-contained HTML file that includes:
- Multiple visualizations
- Titles and labeled axes
- Narrative explanations of each chart

This design ensures that:
- The report can be opened in any browser
- No Python environment is required for viewing
- Insights are clearly communicated without technical knowledge

The reporting layer reads from the pipeline outputs rather than recomputing data, maintaining separation between computation and presentation. This ensures a strict separation between computation (pipeline) and presentation (reporting), improving modularity and maintainability.

---
