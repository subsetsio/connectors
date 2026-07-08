SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ls-oc13"
WHERE value IS NOT NULL
