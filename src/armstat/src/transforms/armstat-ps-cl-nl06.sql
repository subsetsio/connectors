SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-cl-nl06"
WHERE value IS NOT NULL
