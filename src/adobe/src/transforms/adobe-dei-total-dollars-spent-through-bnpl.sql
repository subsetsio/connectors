SELECT date, value
FROM (
    SELECT
        COALESCE(try_strptime("date", '%-m/%-d/%y')::DATE, CASE WHEN try_cast("date" AS INTEGER) IS NOT NULL THEN DATE '1899-12-30' + try_cast("date" AS INTEGER) END) AS date,
        TRY_CAST("Growth" AS DOUBLE) AS value,
        row_number() OVER (PARTITION BY COALESCE(try_strptime("date", '%-m/%-d/%y')::DATE, CASE WHEN try_cast("date" AS INTEGER) IS NOT NULL THEN DATE '1899-12-30' + try_cast("date" AS INTEGER) END) ORDER BY _file_date DESC) AS rn
    FROM "adobe-dei-total-dollars-spent-through-bnpl"
    WHERE "date" IS NOT NULL
)
WHERE rn = 1 AND date IS NOT NULL AND value IS NOT NULL
ORDER BY date
