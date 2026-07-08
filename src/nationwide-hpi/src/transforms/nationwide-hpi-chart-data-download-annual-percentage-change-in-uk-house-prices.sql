SELECT
    CAST(date AS DATE)    AS date,
    period_label,
    category,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "nationwide-hpi-chart-data-download-annual-percentage-change-in-uk-house-prices"
WHERE value IS NOT NULL
