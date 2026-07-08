SELECT
    CAST(date AS DATE)   AS date,
    series,
    CAST(value AS DOUBLE) AS value,
    frequency
FROM "economic-policy-uncertainty-energy-related-uncertainty-indexes"
WHERE value IS NOT NULL AND series IS NOT NULL
