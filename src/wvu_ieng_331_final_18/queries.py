from pathlib import Path
import duckdb
import polars as pl


def _load_sql(file_name: str) -> str:
    sql_path = Path(__file__).parent.parent.parent / "sql" / file_name
    return sql_path.read_text()

def _run_query(sql: str, db_path: str, params=()):
    import duckdb

    conn = duckdb.connect(db_path)

    try:
        result = conn.execute(sql, params).pl()
        return result
    finally:
        conn.close()

def get_seller_scorecard(db_path: str, seller_id: str) -> pl.DataFrame:
    """
    Returns seller scorecard metrics for a given seller.

    Args:
        db_path: Path to DuckDB database
        seller_id: Seller identifier used as SQL parameter

    Returns:
        Polars DataFrame with seller metrics
    """
    sql = _load_sql("seller_scorecard.sql")
    return _run_query(sql, db_path, (seller_id,))

def get_abc_classification(
    db_path: str,
    start_date: str | None = None,
    end_date: str | None = None
):
    """
    Run ABC classification query with optional date filtering.

    Args:
        db_path: Path to DuckDB database
        start_date: Optional start date filter
        end_date: Optional end date filter

    Returns:
        Polars DataFrame with ABC classification results
    """
    sql = _load_sql("abc_classification.sql")

    return _run_query(sql, db_path, (start_date, end_date))