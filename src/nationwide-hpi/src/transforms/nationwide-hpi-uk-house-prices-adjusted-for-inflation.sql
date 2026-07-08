SELECT
    CAST(date AS DATE)    AS date,
    period_label,
    category,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "nationwide-hpi-uk-house-prices-adjusted-for-inflation"
WHERE value IS NOT NULL
