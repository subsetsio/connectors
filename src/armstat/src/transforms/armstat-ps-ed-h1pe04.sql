SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ed-h1pe04"
WHERE value IS NOT NULL
