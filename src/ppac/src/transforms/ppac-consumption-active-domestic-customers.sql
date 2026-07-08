SELECT state,
       TRY_CAST(as_of AS DATE) AS as_of,
       unit,
       CAST(value AS DOUBLE) AS value
FROM "ppac-consumption-active-domestic-customers"
WHERE state IS NOT NULL AND value IS NOT NULL
