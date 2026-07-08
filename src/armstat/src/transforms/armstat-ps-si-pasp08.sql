SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-si-pasp08"
WHERE value IS NOT NULL
