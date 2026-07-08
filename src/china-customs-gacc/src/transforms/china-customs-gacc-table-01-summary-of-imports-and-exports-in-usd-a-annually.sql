SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-01-summary-of-imports-and-exports-in-usd-a-annually"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
