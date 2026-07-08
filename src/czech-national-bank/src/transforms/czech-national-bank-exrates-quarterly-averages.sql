SELECT DISTINCT
    CAST(year AS INTEGER)         AS year,
    month                         AS period,
    currencyCode                  AS currency_code,
    CAST(amount AS INTEGER)       AS amount,
    CAST(average AS DOUBLE)       AS average
FROM "czech-national-bank-exrates-quarterly-averages"
WHERE year IS NOT NULL AND average IS NOT NULL
