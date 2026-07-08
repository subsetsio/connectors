SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ic-ind-marz-06"
WHERE value IS NOT NULL
