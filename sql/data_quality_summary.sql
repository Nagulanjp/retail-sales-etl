-- Count processed rows and the main data-quality flags.
SELECT
    COUNT(*) AS processed_rows,
    SUM(CASE WHEN HasMissingCustomerID THEN 1 ELSE 0 END)
        AS missing_customer_id_rows,
    SUM(CASE WHEN HasMissingDescription THEN 1 ELSE 0 END)
        AS missing_description_rows,
    SUM(CASE WHEN HasZeroUnitPrice THEN 1 ELSE 0 END)
        AS zero_unit_price_rows,
    SUM(CASE
        WHEN TransactionType = 'unpriced_negative_quantity' THEN 1
        ELSE 0
    END) AS unpriced_negative_quantity_rows,
    SUM(CASE
        WHEN TransactionType = 'financial_adjustment' THEN 1
        ELSE 0
    END) AS financial_adjustment_rows
FROM read_parquet('data/processed/retail_transactions.parquet');