SELECT
    CAST(date AS DATE)            AS date,
    currency_code,
    currency_name,
    CAST(rate AS DOUBLE)          AS rate,
    CAST(quant AS BIGINT)         AS quant,
    CAST(rate AS DOUBLE) / NULLIF(CAST(quant AS DOUBLE), 0) AS rate_per_unit,
    CAST(change AS DOUBLE)        AS change,
    direction
FROM "national-bank-fx-rates"
WHERE rate IS NOT NULL
  AND rate > 0                 -- drop meaningless 0 rates (e.g. LTL at 2015 euro changeover)
  AND quant IS NOT NULL
  AND currency_code IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY date, currency_code ORDER BY rate
) = 1
