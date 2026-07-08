SELECT CAST(date AS DATE)   AS date,
       CAST(rate AS DOUBLE) AS rate
FROM "bank-negara-malaysia-kl-usd-reference-rate"
WHERE date IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
