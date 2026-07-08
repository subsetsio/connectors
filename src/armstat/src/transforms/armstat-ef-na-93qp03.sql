SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-na-93qp03"
WHERE value IS NOT NULL
