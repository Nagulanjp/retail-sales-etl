-- Summarize net transaction amounts by country.
SELECT
    Country,
    COUNT(
        DISTINCT CASE
            WHEN TransactionType = 'sale' THEN InvoiceNo
        END
    ) AS sales_invoice_count,
    COUNT(
        DISTINCT CASE
            WHEN TransactionType = 'sale' THEN CustomerID
        END
    ) AS known_customer_count,
    ROUND(SUM(LineTotal), 2) AS net_amount
FROM read_parquet('data/processed/retail_transactions.parquet')
WHERE TransactionType NOT IN (
    'financial_adjustment',
    'unpriced_negative_quantity'
)
GROUP BY Country
ORDER BY net_amount DESC
LIMIT 10;