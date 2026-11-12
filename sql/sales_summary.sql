-- Summarize row counts and signed transaction amounts by type.
SELECT
    TransactionType,
    COUNT(*) AS row_count,
    ROUND(SUM(LineTotal), 2) AS net_amount
FROM read_parquet('data/processed/retail_transactions.parquet')
GROUP BY TransactionType
ORDER BY net_amount DESC;