SELECT
    CAST(date AS DATE)    AS date,
    period_label,
    category,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "nationwide-hpi-ftb-hper-by-broad-occupation"
WHERE value IS NOT NULL
