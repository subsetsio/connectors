SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ls-oc10"
WHERE value IS NOT NULL
