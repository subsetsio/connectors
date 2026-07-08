SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-04-imports-and-exports-by-hs-section-and-division"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
