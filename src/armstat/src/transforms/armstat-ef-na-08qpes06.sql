SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-na-08qpes06"
WHERE value IS NOT NULL
