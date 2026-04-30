import argparse
from pathlib import Path

from loguru import logger

from wvu_ieng_331_m2_18.validation import validate_database
from wvu_ieng_331_m2_18.queries import (
    get_seller_scorecard,
    get_abc_classification,
)


def main():
    parser = argparse.ArgumentParser(description="ETL Pipeline")

    parser.add_argument(
    "--db-path",
    type=str,
    default="data/olist.duckdb",
    help="Path to DuckDB database (default: data/olist.duckdb)"
)
    parser.add_argument("--seller-id", default=None, help="Optional seller filter")
    parser.add_argument("--start-date", default=None, help="Optional start date filter")
    parser.add_argument("--end-date", default=None, help="Optional end date filter")

    args = parser.parse_args()

    logger.info("Starting pipeline...")

    # -----------------------------
    # OUTPUT DIRECTORY SETUP
    # -----------------------------
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # VALIDATION
    # -----------------------------
    if not validate_database(args.db_path):
        logger.error("Validation failed. Stopping pipeline.")
        return

    logger.info("Validation passed")

    # -----------------------------
    # QUERIES
    # -----------------------------

    # ABC classification (required output base)
    df_abc = get_abc_classification(args.db_path)
    logger.info(f"ABC rows: {len(df_abc)}")

    # Optional seller scorecard
    if args.seller_id:
        df_seller = get_seller_scorecard(args.db_path, args.seller_id)
        logger.info(f"Seller scorecard rows: {len(df_seller)}")

    # -----------------------------
    # OUTPUT FILES
    # -----------------------------

    # summary.csv (required)
    summary_path = output_dir / "summary.csv"
    df_abc.write_csv(summary_path)
    logger.info(f"Summary written to {summary_path}")

    # detail.parquet (required)
    detail_path = output_dir / "detail.parquet"
    df_abc.write_parquet(detail_path)
    logger.info(f"Detail written to {detail_path}")

    # chart.html (placeholder visualization)
    chart_path = output_dir / "chart.html"

    # Simple Altair fallback chart
    import altair as alt

    chart = (
        alt.Chart(df_abc.to_pandas())
        .mark_bar()
        .encode(
            x=alt.X(df_abc.columns[0]),
            y=alt.Y(df_abc.columns[1]),
        )
    )

    chart.save(chart_path)
    logger.info(f"Chart written to {chart_path}")

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()

from .report import build_report

# after all pipeline steps finish:
build_report()