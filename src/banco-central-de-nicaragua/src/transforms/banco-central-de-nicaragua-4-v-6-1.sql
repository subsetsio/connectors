SELECT
    CAST(date AS DATE) AS date,
    CAST(year AS INTEGER) AS year,
    CAST(month AS INTEGER) AS month,
    period_label,
    CAST(col_index AS INTEGER) AS col_index,
    CAST(value AS DOUBLE) AS value
FROM "banco-central-de-nicaragua-4-v-6-1"
WHERE value IS NOT NULL
ORDER BY date, col_index
