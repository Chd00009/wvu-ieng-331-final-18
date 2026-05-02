from pathlib import Path
import pandas as pd
import plotly.express as px


def build_report():
    output_dir = Path("output")

    summary_file = output_dir / "summary.csv"
    detail_file = output_dir / "detail.parquet"
    report_file = output_dir / "report.html"

    # Load data
    summary = pd.read_csv(summary_file)
    detail = pd.read_parquet(detail_file)

    # -----------------------------
    # Visualization 1: Revenue Concentration
    # -----------------------------
    fig_time = px.line(
        detail.sort_values("cumulative_pct"),
        x="cumulative_pct",
        y="total_revenue",
        title="Revenue Concentration (ABC Curve)"
    )

    time_html = fig_time.to_html(full_html=False)

    # -----------------------------
    # Visualization 2: ABC Comparison
    # -----------------------------
    abc_counts = detail["abc_class"].value_counts().reindex(["A", "B", "C"])

    fig_bar = px.bar(
        x=abc_counts.index,
        y=abc_counts.values,
        title="Product Count by ABC Class",
        labels={"x": "ABC Class", "y": "Number of Products"}
    )

    bar_html = fig_bar.to_html(full_html=False)

    # -----------------------------
    # Visualization 3: Distribution
    # -----------------------------
    detail["total_revenue"] = pd.to_numeric(detail["total_revenue"], errors="coerce")
    detail = detail.dropna(subset=["total_revenue"])

    fig_hist = px.histogram(
        detail,
        x="total_revenue",
        nbins=60,
        title="Distribution of Product Revenue",
        labels={"total_revenue": "Revenue"}
    )

    fig_hist.update_layout(bargap=0.05)

    hist_html = fig_hist.to_html(full_html=False)

    # -----------------------------
    # Build Report HTML
    # -----------------------------
    html = f"""
    <html>
    <head>
        <title>Olist Business Analysis Report</title>
    </head>
    <body>

    <h1>Olist Business Analysis Report</h1>

    <h2>Business Context</h2>
    <p>
    This analysis explores how revenue is distributed across products in the Olist marketplace.
    The goal is to identify which products drive the majority of business value and understand
    how performance is concentrated across the product catalog.
    </p>

    <h2>Core Insight: Revenue Concentration</h2>
    <p>
    The results show a strong concentration of revenue in a small number of products.
    A-class items dominate total revenue, while B and C-class items form a long tail of lower-impact products.
    This indicates a highly imbalanced revenue structure typical of e-commerce platforms.
    </p>

    <h2>Visualization 1: Revenue Concentration</h2>
    {time_html}
    <p><b>Insight:</b> Revenue accumulation is uneven, with a small number of products contributing disproportionately to total value.</p>

    <h2>Visualization 2: ABC Comparison</h2>
    {bar_html}
    <p><b>Insight:</b> Most products fall into lower-impact categories (B and C), reinforcing that revenue is driven by a small subset of items.</p>

    <h2>Visualization 3: Revenue Distribution</h2>
    {hist_html}
    <p><b>Insight:</b> Revenue is heavily right-skewed, meaning most products generate low revenue while a few generate extremely high values.</p>

    <h2>Recommendations</h2>
    <ul>
        <li>Focus business strategy on scaling A-class products that generate most revenue.</li>
        <li>Investigate C-class products for low demand or inefficiency.</li>
        <li>Use ABC segmentation to guide inventory planning and marketing priorities.</li>
    </ul>

    </body>
    </html>
    """

    report_file.write_text(html, encoding="utf-8")
    print("Report generated:", report_file)


if __name__ == "__main__":
    build_report()