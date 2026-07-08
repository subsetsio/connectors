SELECT CAST(date AS DATE)        AS date,
       CAST(total_sum AS DOUBLE) AS total_sum
FROM "bank-negara-malaysia-fx-turn-over"
WHERE date IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
