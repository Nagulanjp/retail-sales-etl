"""Load the source workbook and print a small first look at its contents."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def main() -> None:
    """Read the retail workbook and summarize its structure and quality."""
    transactions = pd.read_excel(SOURCE_FILE)

    print(f"Source file: {SOURCE_FILE.name}")
    print(f"Rows: {len(transactions):,}")
    print(f"Columns: {len(transactions.columns)}")
    print("Column names:")
    print(", ".join(transactions.columns.astype(str)))
    print("\nFirst five rows:")
    print(transactions.head().to_string(index=False))
    print("\nMissing values by column:")
    print(transactions.isna().sum().to_string())
    print(f"\nDuplicate rows: {transactions.duplicated().sum():,}\n")

    print(f"Rows with quantity <= 0: {(transactions['Quantity'] <= 0).sum():,}")
    print(f"Rows with unit price <= 0: {(transactions['UnitPrice'] <= 0).sum():,}")
    print(f"Cancellation invoices: {transactions['InvoiceNo'].astype(str).str.startswith('C').sum():,}")

    print("\nSample rows with non-positive quantity or price:")
    unusual_rows = transactions.loc[
        (transactions["Quantity"] <= 0) | (transactions["UnitPrice"] <= 0),
        ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"],
    ]
    print(unusual_rows.head(10).to_string(index=False))

    price_columns = ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]

    print("\nRows with negative unit prices:")
    print(
        transactions.loc[transactions["UnitPrice"] < 0, price_columns]
        .head(10)
        .to_string(index=False)
    )

    print("\nRows with zero unit prices:")
    print(
        transactions.loc[transactions["UnitPrice"] == 0, price_columns]
        .head(10)
        .to_string(index=False)
    )

if __name__ == "__main__":
    main()
