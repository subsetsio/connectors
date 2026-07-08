SELECT CAST(date AS DATE)          AS date,
       CAST(overnight AS DOUBLE)   AS overnight,
       CAST(week_1 AS DOUBLE)      AS week_1,
       CAST(week_2 AS DOUBLE)      AS week_2,
       CAST(month_1 AS DOUBLE)     AS month_1,
       CAST(month_2 AS DOUBLE)     AS month_2,
       CAST(month_3 AS DOUBLE)     AS month_3,
       CAST(month_6 AS DOUBLE)     AS month_6,
       CAST(month_9 AS DOUBLE)     AS month_9,
       CAST(month_12 AS DOUBLE)    AS month_12,
       CAST(more_1_year AS DOUBLE) AS more_1_year
FROM "bank-negara-malaysia-interbank-swap"
WHERE date IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
