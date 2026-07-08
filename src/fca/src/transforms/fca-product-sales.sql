SELECT grouped_by,
       category,
       subcategory,
       period,
       CAST(regexp_extract(period, '(\d{4})', 1) AS INTEGER) AS year,
       regexp_extract(period, '^(Q[1-4])', 1) AS quarter,
       CAST(no_of_sales AS DOUBLE) AS no_of_sales
FROM "fca-product-sales"
WHERE no_of_sales IS NOT NULL AND period IS NOT NULL
