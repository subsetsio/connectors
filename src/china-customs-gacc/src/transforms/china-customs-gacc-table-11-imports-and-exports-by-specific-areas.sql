SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-11-imports-and-exports-by-specific-areas"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
