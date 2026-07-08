SELECT date, value
FROM (
    SELECT
        COALESCE(try_strptime("Date", '%-m/%-d/%y')::DATE, CASE WHEN try_cast("Date" AS INTEGER) IS NOT NULL THEN DATE '1899-12-30' + try_cast("Date" AS INTEGER) END) AS date,
        TRY_CAST("Spend in billions" AS DOUBLE) AS value,
        row_number() OVER (PARTITION BY COALESCE(try_strptime("Date", '%-m/%-d/%y')::DATE, CASE WHEN try_cast("Date" AS INTEGER) IS NOT NULL THEN DATE '1899-12-30' + try_cast("Date" AS INTEGER) END) ORDER BY _file_date DESC) AS rn
    FROM "adobe-dei-buy-now-pay-later-monthly-spend"
    WHERE "Date" IS NOT NULL
)
WHERE rn = 1 AND date IS NOT NULL AND value IS NOT NULL
ORDER BY date
