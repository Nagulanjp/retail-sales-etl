
# Databricks Lakehouse Data Pipeline

A retail data pipeline built with PySpark, Delta Lake, and Spark SQL in Databricks Free Edition. It follows the Medallion Architecture to turn raw transactions into business-ready summaries.

## Architecture

- **Bronze:** Ingests the source CSV with minimal changes and stores it as a Delta table.
- **Silver:** Removes exact duplicate rows, applies data types, calculates line totals, classifies transactions, adds data-quality flags, and trims descriptions.
- **Gold:** Creates summary tables for monthly sales, country sales, and product sales.

## Dataset

The pipeline uses the UCI Online Retail dataset. The source workbook was converted to CSV for upload to Databricks.

The dataset contains 541,909 source rows. After removing 5,268 exact duplicates, the Silver table contains 536,641 rows.

## Delta Lake

The Silver table’s history records the table creation and subsequent operations. A time-travel comparison showed:


| Snapshot                  |    Rows | Descriptions needing trim |
| --------------------------- | --------: | --------------------------: |
| Version 0, before cleanup | 536,641 |                   111,983 |
| Current, after cleanup    | 536,641 |                         0 |

This demonstrates that the cleanup changed descriptions while preserving the row count.

## Gold tables

- `gold_monthly_sales` — monthly invoice counts, known customer counts, gross sales, and net sales.
- `gold_country_sales` — sales metrics by country.
- `gold_product_sales` — net sales by product, with the most common sale description.

## Technologies

- Databricks Free Edition serverless compute
- PySpark
- Delta Lake
- Spark SQL

## Run environment

The pipeline was developed and run in a Databricks notebook using Free Edition serverless compute. No user-managed cluster was configured.

## Data and privacy

The source dataset is not included in this repository. Upload the CSV to a Unity Catalog volume before running the notebook. Do not commit the dataset or any account credentials.

## Notebook

See [`Databricks_Lakehouse_Data_Pipeline.ipynb`](Databricks_Lakehouse_Data_Pipeline.ipynb) for the pipeline steps and SQL analyses.~~~~
