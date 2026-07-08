SELECT currency_code,
       CAST(unit AS INTEGER)        AS unit,
       CAST(date AS DATE)           AS date,
       CAST(buying_rate AS DOUBLE)  AS buying_rate,
       CAST(selling_rate AS DOUBLE) AS selling_rate
FROM "bank-negara-malaysia-exchange-rate"
WHERE date IS NOT NULL AND currency_code IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY currency_code, date ORDER BY date) = 1
