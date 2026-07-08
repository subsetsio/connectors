SELECT
    CAST(date AS DATE)    AS date,
    period_label,
    category,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "nationwide-hpi-annual-percentage-change-in-regional-house-prices"
WHERE value IS NOT NULL
