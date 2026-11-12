# Cleaning rules

- Keep the original workbook unchanged in `data/raw`.
- Remove exact duplicate rows from the processed data.
- Calculate `LineTotal` as `Quantity * UnitPrice`, preserving negative values.
- Classify invoices whose number starts with `C` as cancellations and retain them.
- Classify non-cancellation rows with negative quantities and positive unit prices as returns.
- Classify rows with negative quantities and zero unit prices as `unpriced_negative_quantity`; retain them without assuming they are returns.
- Identify “Adjust bad debt” rows as financial adjustments and keep them out of product sales metrics.
- Keep rows with missing customer IDs or descriptions, and flag the missing values.
- Exclude missing customer IDs only from analyses that require identifying individual customers.
- Keep zero-price rows and flag them.
