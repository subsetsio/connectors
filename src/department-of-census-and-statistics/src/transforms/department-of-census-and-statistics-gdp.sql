SELECT CAST(date AS DATE) AS date,
       period,
       frequency,
       price_basis,
       measure,
       sector_code,
       sector_title,
       sector_group,
       CAST(value AS DOUBLE) AS value
FROM "department-of-census-and-statistics-gdp"
WHERE value IS NOT NULL
