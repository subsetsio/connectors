SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-af-1-2024"
WHERE value IS NOT NULL
