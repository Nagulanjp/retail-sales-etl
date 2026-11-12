from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "retail_transactions.parquet"


def extract_data() -> pd.DataFrame:
    """Read and return the raw retail workbook."""
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Could not find source file: {SOURCE_FILE}")

    return pd.read_excel(SOURCE_FILE)


def transform_data(transactions: pd.DataFrame) -> pd.DataFrame:
    """Clean, classify, and enrich transactions while keeping every row."""
    deduplicated = transactions.copy()

    # These fields are identifiers or descriptions, so store them as text.
    # This also gives Parquet a consistent type for each column.
    deduplicated["InvoiceNo"] = deduplicated["InvoiceNo"].astype("string")
    deduplicated["StockCode"] = deduplicated["StockCode"].astype("string")
    deduplicated["Description"] = deduplicated["Description"].astype("string")

    # Remove rows only when every original field is an exact duplicate.
    deduplicated = deduplicated.drop_duplicates().copy()

    # Calculate the signed value of each transaction line.
    deduplicated["LineTotal"] = (
        deduplicated["Quantity"] * deduplicated["UnitPrice"]
    )

    # Start by treating rows as sales, then apply more specific labels.
    deduplicated["TransactionType"] = "sale"

    deduplicated.loc[
        (deduplicated["Quantity"] < 0)
        & (deduplicated["UnitPrice"] == 0),
        "TransactionType",
    ] = "unpriced_negative_quantity"

    deduplicated.loc[
        (deduplicated["Quantity"] < 0)
        & (deduplicated["UnitPrice"] > 0),
        "TransactionType",
    ] = "return"

    deduplicated.loc[
        deduplicated["InvoiceNo"].str.startswith("C", na=False),
        "TransactionType",
    ] = "cancellation"

    deduplicated.loc[
        deduplicated["Description"].eq("Adjust bad debt"),
        "TransactionType",
    ] = "financial_adjustment"

    # Keep rows with missing or zero-value data, but make them easy to identify.
    deduplicated["HasMissingCustomerID"] = deduplicated["CustomerID"].isna()
    deduplicated["HasMissingDescription"] = deduplicated["Description"].isna()
    deduplicated["HasZeroUnitPrice"] = deduplicated["UnitPrice"].eq(0)

    return deduplicated


if __name__ == "__main__":
    transactions = extract_data()
    cleaned_transactions = transform_data(transactions)

    duplicates_removed = len(transactions) - len(cleaned_transactions)

    print(f"Loaded rows: {len(transactions):,}")
    print(f"Rows after removing exact duplicates: {len(cleaned_transactions):,}")
    print(f"Exact duplicates removed: {duplicates_removed:,}")

    print("\nTransaction counts by type:")
    print(cleaned_transactions["TransactionType"].value_counts().to_string())

    print("\nData-quality flag counts:")
    print(
        f"Missing customer IDs: "
        f"{cleaned_transactions['HasMissingCustomerID'].sum():,}"
    )
    print(
        f"Missing descriptions: "
        f"{cleaned_transactions['HasMissingDescription'].sum():,}"
    )
    print(
        f"Zero unit prices: "
        f"{cleaned_transactions['HasZeroUnitPrice'].sum():,}"
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned_transactions.to_parquet(OUTPUT_FILE, index=False)

    print(f"\nSaved curated data to: {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
    print(f"Saved rows: {len(cleaned_transactions):,}")