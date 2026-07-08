SELECT
    CAST(ccode AS INTEGER) AS ccode,
    country,
    CAST(year AS INTEGER)  AS year,
    CAST(value AS DOUBLE)  AS value
FROM "clio-infra-exchangeratestousdollar"
WHERE value IS NOT NULL AND year IS NOT NULL
