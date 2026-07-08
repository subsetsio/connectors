SELECT
    CAST(date AS DATE) AS date,
    series,
    CAST(value AS DOUBLE) AS value,
    period
FROM "bank-of-estonia-3459"
WHERE date IS NOT NULL AND value IS NOT NULL
