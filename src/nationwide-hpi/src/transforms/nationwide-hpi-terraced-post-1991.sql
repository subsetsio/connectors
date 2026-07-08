SELECT
    CAST(date AS DATE)    AS date,
    period_label,
    category,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "nationwide-hpi-terraced-post-1991"
WHERE value IS NOT NULL
