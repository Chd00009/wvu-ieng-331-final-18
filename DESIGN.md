# Design Rationale

## Parameter Flow

The `--start-date` and `--end-date` parameters directly affect the ABC classification query by filtering `order_purchase_timestamp` in `abc_classification.sql` using parameterized SQL conditions ($1 and $2). These values are passed from `pipeline.py` into `queries.py`, where they are bound to the DuckDB query execution. This ensures that the dataset can be dynamically filtered at runtime without modifying SQL logic.

```python
parser.add_argument("--seller-id", default=None)
```
After parsing, all arguments are stored in the args object. For example, args.seller_id holds the value passed by the user.

This value is then passed into the data access layer. In pipeline.py, the function call:
df_seller = get_seller_scorecard(args.db_path, args.seller_id)
sends the parameter into the queries.py module. Inside queries.py, the value is passed as a parameter when executing the SQL query.

This design allows command-line inputs to directly influence the database query results without modifying SQL code, making the pipeline flexible and reusable.

## SQL Parameterization

An example SQL file is seller_scorecard.sql, which contains a query using parameter placeholders:
SELECT *
FROM sellers
WHERE seller_id = $1;
The $1 represents a parameter that will be replaced at runtime.

In queries.py, the SQL file is read using pathlib, and then executed like this:
conn.execute(sql, [seller_id])
The value of seller_id is passed safely into the query.

Parameterized queries are used instead of f-strings or string concatenation because they prevent SQL injection and ensure that user input does not alter the structure of the query.

SQL is stored in .sql files instead of inside Python code to improve organization and maintainability. This keeps query logic separate from application logic and makes it easier to update queries without modifying Python functions.

## Validation Logic

Validation is implemented in the validate_database() function in validation.py.

The main validation step checks that all required tables exist in the database. These include:

orders
order_items
customers
products
sellers
geolocation
order_payments
order_reviews
category_translation

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
