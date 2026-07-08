SELECT CAST(date AS DATE) AS date,
       period,
       measure,
       category_code,
       category_title,
       weight,
       base_value,
       CAST(value AS DOUBLE) AS value
FROM "department-of-census-and-statistics-ncpi"
WHERE value IS NOT NULL
