SELECT CAST(period AS DATE) AS date,
       financial_year,
       section,
       item,
       unit,
       CAST(value AS DOUBLE) AS value
FROM "ppac-production-crude-processing"
WHERE value IS NOT NULL
