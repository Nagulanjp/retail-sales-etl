-- Rank products by net sales after cancellations.
SELECT
    StockCode,
    COALESCE(MAX(Description), 'Unknown description') AS ProductDescription,
    ROUND(SUM(LineTotal), 2) AS NetSales
FROM read_parquet('data/processed/retail_transactions.parquet')
WHERE TransactionType NOT IN (
    'financial_adjustment',
    'unpriced_negative_quantity'
) AND StockCode NOT IN ('DOT', 'POST', '23084')
GROUP BY StockCode
ORDER BY NetSales DESC
LIMIT 10;