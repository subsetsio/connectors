SELECT
    CAST(date AS DATE)    AS date,
    period_label,
    category,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "nationwide-hpi-uk-house-price-since-1952"
WHERE value IS NOT NULL
