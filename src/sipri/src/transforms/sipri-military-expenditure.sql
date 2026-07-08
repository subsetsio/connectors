SELECT
    country,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "sipri-military-expenditure"
WHERE value IS NOT NULL
