# Retail Sales ETL Data Pipeline

A local-first portfolio project that ingests retail transaction data, validates and transforms it with Python and pandas, writes analysis-ready output, and supports SQL analytics. AWS S3, Glue, and Athena are optional later stages; local development does not require an AWS account.

## Project structure

- `data/raw/` — source files (kept out of Git)
- `data/processed/` — generated outputs (kept out of Git)
- `src/` — pipeline code
- `sql/` — analysis queries
- `tests/` — checks added in a later stage
- `docs/` — architecture and project notes

## Getting started

1. Create and activate a virtual environment: `python -m venv .venv`
2. Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
3. Install dependencies: `python -m pip install -r requirements.txt`

Dataset setup and pipeline implementation are part of the next stages.

## Run the project locally

### 1. Get the dataset

Download the UCI Online Retail workbook using the source and attribution details in `docs/dataset.md`. Place it at:

`data/raw/Online Retail.xlsx`

The raw data is excluded from Git, so each person setting up the project needs to download it.

### 2. Set up Python

From the project folder, open a terminal and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 3. Build the processed dataset

python src/etl.py
This removes exact duplicate rows, adds transaction labels and data-quality flags, calculates line totals, and writes data/processed/retail_transactions.parquet.

### 4. Run a SQL analysis

In src/run_sql.py, set QUERY_FILE to the SQL file you want to run, such as sql/monthly_sales.sql. Then run:
python src/run_sql.py
Available analyses are in the sql/ folder.
