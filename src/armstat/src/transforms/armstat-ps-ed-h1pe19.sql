SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ed-h1pe19"
WHERE value IS NOT NULL
