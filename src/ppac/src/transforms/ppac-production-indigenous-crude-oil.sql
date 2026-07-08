SELECT CAST(period AS DATE) AS date,
       financial_year,
       section,
       item,
       unit,
       CAST(value AS DOUBLE) AS value
FROM "ppac-production-indigenous-crude-oil"
WHERE value IS NOT NULL
