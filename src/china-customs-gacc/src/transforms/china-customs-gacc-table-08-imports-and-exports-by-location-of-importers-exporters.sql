SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-08-imports-and-exports-by-location-of-importers-exporters"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
