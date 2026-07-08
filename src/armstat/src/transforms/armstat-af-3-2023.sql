SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-af-3-2023"
WHERE value IS NOT NULL
