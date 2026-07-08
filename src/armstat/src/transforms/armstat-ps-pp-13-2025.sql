SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-pp-13-2025"
WHERE value IS NOT NULL
