SELECT product,
       CAST(date AS DATE)        AS date,
       CAST(overnight AS DOUBLE) AS overnight,
       CAST(week_1 AS DOUBLE)    AS week_1,
       CAST(month_1 AS DOUBLE)   AS month_1,
       CAST(month_3 AS DOUBLE)   AS month_3,
       CAST(month_6 AS DOUBLE)   AS month_6,
       CAST(year_1 AS DOUBLE)    AS year_1,
       CAST(other AS DOUBLE)     AS other
FROM "bank-negara-malaysia-interest-volume"
WHERE date IS NOT NULL AND product IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY product, date ORDER BY date) = 1
