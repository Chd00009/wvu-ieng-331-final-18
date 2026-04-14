from loguru import logger
import duckdb


def validate_database(db_path: str) -> bool:
    """
    Runs validation checks on the DuckDB database.

    Args:
        db_path: Path to DuckDB database file

    Returns:
        True if all validations pass, False otherwise
    """
    try:
        conn = duckdb.connect(db_path)

        logger.info("Running validation checks...")

        # REQUIRED TABLES (MATCHES YOUR ACTUAL DATASET)
        required_tables = {
            "orders",
            "order_items",
            "customers",
            "products",
            "sellers",
            "geolocation",
            "order_payments",
            "order_reviews",
            "category_translation"
        }

        # FETCH ACTUAL TABLES
        tables = conn.execute("""
            SELECT table_name
            FROM information_schema.tables
        """).fetchall()

        table_names = {t[0] for t in tables}

        # CHECK MISSING TABLES
        missing = required_tables - table_names

        if missing:
            logger.warning(f"Missing tables: {missing}")
            return False

        logger.info("All required tables exist")

        conn.close()
        return True

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return False