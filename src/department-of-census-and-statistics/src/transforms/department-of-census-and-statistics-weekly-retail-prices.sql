SELECT CAST(date AS DATE) AS date,
       week_label,
       product,
       product_name,
       category,
       CAST(price_lkr AS DOUBLE) AS price_lkr
FROM "department-of-census-and-statistics-weekly-retail-prices"
WHERE price_lkr IS NOT NULL
