from pathlib import Path
import pandas as pd
import plotly.express as px

def build_report():
    output_dir = Path("output")

    summary_file = output_dir / "summary.csv"
    detail_file = output_dir / "detail.parquet"
    chart_file = output_dir / "chart.html"

    report_file = output_dir / "report.html"

    # Load data
    summary = pd.read_csv(summary_file)
    detail = pd.read_parquet(detail_file)

    # --- Visualization 2: Category Comparison ---
    category_counts = detail.iloc[:, 0].value_counts().head(10)
    fig_bar = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        title="Top 10 Categories by Count"
    )
    bar_html = fig_bar.to_html(full_html=False)

    # --- Visualization 3: Distribution ---
    fig_hist = px.histogram(
        detail.iloc[:, 0],
        nbins=30,
        title="Distribution of Key Variable"
    )
    hist_html = fig_hist.to_html(full_html=False)

    # --- Build Report ---
    html = f"""
    <html>
    <head>
        <title>Olist Business Analysis Report</title>
    </head>
    <body>

    <h1>Olist Business Analysis</h1>

    <h2>Overview</h2>
    <p>
    This report analyzes trends, category performance, and distribution patterns
    within the Olist dataset to identify business insights and opportunities.
    </p>

    <h2>Key Findings</h2>
<ul>
    <li>Order activity shows noticeable variation over time, suggesting potential seasonality or shifts in demand.</li>
    <li>A small number of categories account for a large portion of activity, indicating concentration of sales in key segments.</li>
    <li>The distribution of values reveals clustering, which may indicate typical customer behavior patterns as well as outliers worth further investigation.</li>
</ul>

    <h2>Visualization 1: Trend Over Time</h2>
    <iframe src="chart.html" width="100%" height="500"></iframe>
    <p><b>Insight:</b> This shows how activity changes over time.</p>

    <h2>Visualization 2: Category Comparison</h2>
    {bar_html}
    <p><b>Insight:</b> This compares category-level performance.</p>

    <h2>Visualization 3: Distribution</h2>
    {hist_html}
    <p><b>Insight:</b> This shows how values are distributed.</p>

 <h2>Recommendations</h2>
<ul>
    <li>Focus on high-performing categories to identify opportunities for expansion and targeted marketing strategies.</li>
    <li>Investigate time-based trends to better understand seasonality and optimize inventory or logistics planning.</li>
    <li>Analyze outliers in the data to detect potential operational inefficiencies or unusual customer behavior.</li>
</ul>

    </body>
    </html>
    """

    report_file.write_text(html, encoding="utf-8")
    print("Report generated:", report_file)


if __name__ == "__main__":
    build_report()