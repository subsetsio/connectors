SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-na-93qp10"
WHERE value IS NOT NULL
