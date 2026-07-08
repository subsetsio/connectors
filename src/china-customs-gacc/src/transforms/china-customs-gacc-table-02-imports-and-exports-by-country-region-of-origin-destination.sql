SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-02-imports-and-exports-by-country-region-of-origin-destination"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
