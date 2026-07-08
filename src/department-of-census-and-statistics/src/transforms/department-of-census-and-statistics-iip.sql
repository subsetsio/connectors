SELECT CAST(date AS DATE) AS date,
       period,
       category_code,
       category_title,
       CAST(value AS DOUBLE) AS value
FROM "department-of-census-and-statistics-iip"
WHERE value IS NOT NULL
