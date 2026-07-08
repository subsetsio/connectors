SELECT CAST(decimal_date AS DOUBLE) AS year,
       CAST(value AS DOUBLE)        AS co2
FROM "scripps-co2-mlo-spo-annual-mean"
WHERE value IS NOT NULL
