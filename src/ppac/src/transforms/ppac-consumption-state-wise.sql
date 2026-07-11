SELECT product,
       region,
       state,
       fiscal_year,
       unit,
       CAST(value AS DOUBLE) AS value
FROM "ppac-consumption-state-wise"
WHERE value IS NOT NULL
