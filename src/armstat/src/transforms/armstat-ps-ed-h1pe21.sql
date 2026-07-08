SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ed-h1pe21"
WHERE value IS NOT NULL
