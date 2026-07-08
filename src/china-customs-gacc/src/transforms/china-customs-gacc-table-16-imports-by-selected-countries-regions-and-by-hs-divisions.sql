SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-16-imports-by-selected-countries-regions-and-by-hs-divisions"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
