SELECT metric,
       fiscal_year,
       unit,
       CAST(value AS DOUBLE) AS value
FROM "ppac-natural-gas-import"
WHERE value IS NOT NULL
