SELECT DISTINCT
    CAST(date AS DATE) AS date,
    "table" AS rate_table,
    code AS currency_code,
    currency AS currency_name,
    CAST(mid AS DOUBLE) AS mid
FROM "narodowy-bank-polski-exchange-rates-mid"
WHERE mid IS NOT NULL
