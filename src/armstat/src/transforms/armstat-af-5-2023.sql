SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-af-5-2023"
WHERE value IS NOT NULL
