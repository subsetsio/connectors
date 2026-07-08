SELECT
    source_table,
    table_title,
    quotation,
    period,
    period_type,
    CAST(value AS DOUBLE) AS value
FROM "icac-cotton-prices"
WHERE value IS NOT NULL
