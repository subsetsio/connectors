SELECT
    CAST(date AS DATE) AS date,
    series,
    CAST(value AS DOUBLE) AS value,
    period
FROM "bank-of-estonia-4841"
WHERE date IS NOT NULL AND value IS NOT NULL
