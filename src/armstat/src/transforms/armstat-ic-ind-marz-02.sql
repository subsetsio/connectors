SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ic-ind-marz-02"
WHERE value IS NOT NULL
