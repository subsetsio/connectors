SELECT CAST(date AS DATE)           AS date,
       CAST(highest_rate AS DOUBLE) AS highest_rate,
       CAST(lowest_rate AS DOUBLE)  AS lowest_rate
FROM "bank-negara-malaysia-usd-interbank-intraday-rate"
WHERE date IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
