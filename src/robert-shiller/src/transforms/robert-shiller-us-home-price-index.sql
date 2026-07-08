SELECT
    CAST(date AS DATE) AS date,
    series,
    CAST(value AS DOUBLE) AS value
FROM "robert-shiller-us-home-price-index"
WHERE value IS NOT NULL
ORDER BY series, date
