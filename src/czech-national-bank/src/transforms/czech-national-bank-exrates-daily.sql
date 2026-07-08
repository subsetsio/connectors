SELECT DISTINCT
    CAST(validFor AS DATE)        AS date,
    currencyCode                  AS currency_code,
    CAST(amount AS INTEGER)       AS amount,
    CAST(rate AS DOUBLE)          AS rate
FROM "czech-national-bank-exrates-daily"
WHERE validFor IS NOT NULL AND rate IS NOT NULL
