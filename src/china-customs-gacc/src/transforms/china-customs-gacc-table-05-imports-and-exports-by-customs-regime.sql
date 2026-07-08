SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-05-imports-and-exports-by-customs-regime"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
