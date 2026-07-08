SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ed-h2pe06"
WHERE value IS NOT NULL
