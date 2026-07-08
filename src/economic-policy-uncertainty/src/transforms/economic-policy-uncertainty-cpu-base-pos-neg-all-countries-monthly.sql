SELECT
    CAST(date AS DATE)   AS date,
    series,
    CAST(value AS DOUBLE) AS value,
    frequency
FROM "economic-policy-uncertainty-cpu-base-pos-neg-all-countries-monthly"
WHERE value IS NOT NULL AND series IS NOT NULL
