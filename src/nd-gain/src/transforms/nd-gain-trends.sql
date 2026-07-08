SELECT
    iso3,
    country,
    measure,
    CAST(value AS DOUBLE) AS value,
    CAST(sign AS INTEGER) AS sign
FROM "nd-gain-trends"
WHERE value IS NOT NULL
