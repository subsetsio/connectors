SELECT
    currency_code,
    currency_name,
    CAST(quant AS BIGINT) AS quant,
    CAST(source_date AS DATE) AS source_date
FROM "national-bank-currencies"
WHERE currency_code IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY currency_code ORDER BY source_date DESC NULLS LAST
) = 1
