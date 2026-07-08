SELECT CAST(date AS DATE) AS date,
       year,
       period,
       indicator_code,
       indicator_title,
       units,
       CAST(value AS DOUBLE) AS value
FROM "department-of-census-and-statistics-glance-tnteach"
WHERE value IS NOT NULL
