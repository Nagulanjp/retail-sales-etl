# Retail Sales ETL Data Pipeline

A local-first data engineering project that cleans retail transactions with Python and pandas, writes a curated Parquet dataset, and supports SQL analysis with DuckDB. The curated data can also be stored in Amazon S3, cataloged with AWS Glue, and queried with Amazon Athena.

## Architecture

```text
Online Retail.xlsx
       |
       v
Python + pandas ETL (local)
       |
       v
retail_transactions.parquet
       |
       +------> DuckDB SQL analysis (local)
       |
       +------> Amazon S3
                   |
                   v
            AWS Glue Data Catalog
                   |
                   v
              Amazon Athena


The transformation runs locally in src/etl.py. The AWS Glue crawler discovers the Parquet schema and creates table metadata; it does not perform the transformation.
Project structure
- data/raw/ — source workbook; excluded from Git
- data/processed/ — generated Parquet output; excluded from Git
- src/ — ETL and SQL runner code
- sql/ — analysis queries
- docs/ — dataset attribution, cleaning rules, and architecture notes
Dataset
This project uses the UCI Online Retail workbook. See [`docs/dataset.md`](docs/dataset.md) for the source and attribution.

Place the downloaded workbook here:
data/raw/Online Retail.xlsx
The source data is excluded from Git. Anyone setting up the project must download it separately.
Local setup
From the project folder, run these commands in PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Run the ETL
python src/etl.py
The pipeline removes exact duplicate rows, labels transaction types, adds data-quality flags, calculates LineTotal, and writes:
data/processed/retail_transactions.parquet
Processing results
- Source rows: 541,909
- Exact duplicate rows removed: 5,268
- Curated rows: 536,641
Transaction types in the curated data:
Transaction type	Rows
Sale	526,051
Cancellation	9,251
Unpriced negative quantity	1,336
Financial adjustment	3


Run local SQL analysis
In src/run_sql.py, set QUERY_FILE to the SQL file you want to run, then run:
python src/run_sql.py
Available analyses include transaction totals, top products, sales by country, monthly sales, and data-quality summaries. See the sql/ folder.
AWS implementation
The AWS demonstration uses:
- Amazon S3 to store the raw workbook and curated Parquet file in separate prefixes.
- AWS Glue Data Catalog to catalog the curated Parquet data with an on-demand crawler.
- Amazon Athena to run SQL queries against the cataloged table.
The crawler targets only the curated S3 prefix. It created the database retail_sales_db and table curated, with a 13-column schema. Athena query results use a separate S3 prefix.

AWS resources are account-specific and are not created by the local ETL commands. Do not put AWS credentials, account IDs, or private configuration in this repository.
Validation
The curated Parquet file was read locally and queried with DuckDB. The same transaction totals and product net-sales results were checked in Athena. The top-products analysis groups by stock code and uses the most common description for display, so unusual description values do not split a product across multiple result rows.
```
