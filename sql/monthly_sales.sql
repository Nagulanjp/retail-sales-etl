-- Summarize net transaction amounts by month.
SELECT
    CAST(DATE_TRUNC('month', InvoiceDate) AS DATE) AS sales_month,
    COUNT(
        DISTINCT CASE
            WHEN TransactionType = 'sale' THEN InvoiceNo
        END
    ) AS sales_invoice_count,
    ROUND(SUM(LineTotal), 2) AS net_amount
FROM read_parquet('data/processed/retail_transactions.parquet')
WHERE TransactionType NOT IN (
    'financial_adjustment',
    'unpriced_negative_quantity'
)
GROUP BY 1
ORDER BY 1;