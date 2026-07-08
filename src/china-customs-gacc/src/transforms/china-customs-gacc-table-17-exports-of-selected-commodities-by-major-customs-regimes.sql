SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-17-exports-of-selected-commodities-by-major-customs-regimes"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
