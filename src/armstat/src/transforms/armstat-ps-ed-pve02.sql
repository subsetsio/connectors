SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ed-pve02"
WHERE value IS NOT NULL
