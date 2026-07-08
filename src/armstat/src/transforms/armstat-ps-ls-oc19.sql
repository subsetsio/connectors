SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ls-oc19"
WHERE value IS NOT NULL
