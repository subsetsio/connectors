SELECT DISTINCT
    year,
    month,
    period_label,
    col_header AS indicator,
    value
FROM "china-customs-gacc-table-12-imports-and-exports-by-foreign-invested-enterprises"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND period_label <> ''
