SELECT area, period, CAST(period_num AS INTEGER) AS period_num,
       CAST(year AS INTEGER) AS year,
       CAST(cpi_index AS DOUBLE) AS cpi_index,
       CAST(pct_change_12mo AS DOUBLE) AS pct_change_12mo
FROM "alaska-department-of-labor-and-workforce-development-consumer-price-index"
WHERE year IS NOT NULL AND cpi_index IS NOT NULL
