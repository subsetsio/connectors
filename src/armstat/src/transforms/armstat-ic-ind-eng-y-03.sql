SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ic-ind-eng-y-03"
WHERE value IS NOT NULL
