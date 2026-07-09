SELECT
    CAST(row_label AS VARCHAR)   AS row_label,
    CAST(col_label AS VARCHAR)   AS col_label,
    TRY_CAST(period_year AS INTEGER) AS period_year,
    TRY_CAST(value AS DOUBLE)    AS value,
    CAST(value_text AS VARCHAR)  AS value_text
FROM "central-bank-of-sri-lanka-table-2.28"
WHERE value IS NOT NULL
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
  AND row_label IS NOT NULL
  AND TRIM(row_label) <> ''
