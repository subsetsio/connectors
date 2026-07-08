SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-09-imports-and-exports-by-location-of-domestic-consumers-producers"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
