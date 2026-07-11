WITH parsed AS (
    SELECT
        currency_name AS currency,
        try_strptime(post_date, '%d-%b-%y')::DATE AS date,
        TRY_CAST(REPLACE(buying_rate, ',', '') AS DOUBLE) AS buying_rate,
        TRY_CAST(REPLACE(average_rate, ',', '') AS DOUBLE) AS average_rate,
        TRY_CAST(REPLACE(selling_rate, ',', '') AS DOUBLE) AS selling_rate
    FROM "national-bank-of-rwanda-exchange-rates"
    WHERE post_date IS NOT NULL
)
SELECT currency, date, buying_rate, average_rate, selling_rate
FROM (
    SELECT *, row_number() OVER (PARTITION BY currency, date ORDER BY average_rate) AS rn
    FROM parsed
    WHERE date IS NOT NULL AND average_rate IS NOT NULL AND average_rate > 0
)
WHERE rn = 1
