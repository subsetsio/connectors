SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-13-major-export-commodities-in-quantity-and-value"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
