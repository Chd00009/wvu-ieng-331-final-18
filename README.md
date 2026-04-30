# Final Deliverable: Data Pipeline & Analytical Report

**Team 18**: Christopher D'Antonio

---

## Overview

This project implements a complete end-to-end data pipeline for the Olist e-commerce dataset. The system performs data validation, transformation, analysis, and generates a final stakeholder-ready report.

The pipeline is fully automated and produces both intermediate data products and a final self-contained HTML report designed for non-technical users.

---

## How to Run

From a fresh clone of the repository:

```bash
git clone https://github.com/Chd00009/wvu-ieng-331-final-18.git
cd wvu-ieng-331-final-18
uv sync
uv run python -m src.wvu_ieng_331_final_18.pipeline
```
---

## Outputs

The pipeline generates the following files in the `output/` directory:

### summary.csv
Aggregated results from the ABC classification analysis, providing a high-level summary of business performance.

### detail.parquet
Full detailed dataset used for deeper analysis and reproducibility.

### chart.html
Interactive exploratory visualization generated from the dataset.

### report.html (Final Deliverable)
A self-contained HTML report that includes:
- Key business insights
- Three required visualizations
- Narrative interpretation of results

This file can be opened directly in any web browser without requiring Python or additional dependencies.

## Visualizations

The final report includes three distinct analytical visualizations:

1. Time Series Analysis
 - Shows how business activity changes over time
 - Used to identify trends and potential seasonality
2. Category Comparison
 - Highlights differences across product or category groups
 - Identifies dominant segments
3. Distribution Analysis
 - Shows spread and clustering of key metrics
 - Helps identify outliers and typical behavior patterns

## Pipeline Validation

Before execution, the pipeline validates:

 - Presence of all required tables (orders, order_items, customers, products, sellers, geolocation, payments, reviews, category_translation)
 - Schema consistency and dataset integrity
 - Holdout-safe assumptions (no reliance on fixed row counts or date ranges)

If validation fails, execution stops immediately.

## Analytical Summary

The pipeline performs an ABC classification analysis to segment data based on contribution to overall value:

 - A-class items: High-impact contributors
 - B-class items: Moderate contributors
 - C-class items: Low-impact contributors

This segmentation helps identify key drivers of business performance and areas for optimization.

## Design Choice

An HTML-based report was selected as the final deliverable because it:

 - Is fully self-contained
 - Requires no installation or dependencies to view
 - Can be opened in any browser
 - Combines narrative and visualizations in a single file

This makes it suitable for direct stakeholder communication.

## Limitations

 - The pipeline assumes a consistent Olist dataset schema.
 - Filtering parameters exist but may not affect all queries depending on implementation.
 - The report is descriptive rather than predictive or causal.
 - No automated recovery from corrupted or missing data files.
