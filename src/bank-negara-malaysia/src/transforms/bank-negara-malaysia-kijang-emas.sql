SELECT CAST(date AS DATE)                 AS date,
       CAST(one_oz_buying AS DOUBLE)      AS one_oz_buying,
       CAST(one_oz_selling AS DOUBLE)     AS one_oz_selling,
       CAST(half_oz_buying AS DOUBLE)     AS half_oz_buying,
       CAST(half_oz_selling AS DOUBLE)    AS half_oz_selling,
       CAST(quarter_oz_buying AS DOUBLE)  AS quarter_oz_buying,
       CAST(quarter_oz_selling AS DOUBLE) AS quarter_oz_selling
FROM "bank-negara-malaysia-kijang-emas"
WHERE date IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
