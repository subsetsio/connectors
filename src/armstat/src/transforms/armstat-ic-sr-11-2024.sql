SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ic-sr-11-2024"
WHERE value IS NOT NULL
