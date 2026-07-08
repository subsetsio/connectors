SELECT
    CAST(date AS DATE)   AS date,
    series,
    CAST(value AS DOUBLE) AS value,
    frequency
FROM "economic-policy-uncertainty-state-policy-uncertainty"
WHERE value IS NOT NULL AND series IS NOT NULL
