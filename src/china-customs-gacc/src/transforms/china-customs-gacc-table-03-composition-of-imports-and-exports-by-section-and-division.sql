SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-03-composition-of-imports-and-exports-by-section-and-division"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
