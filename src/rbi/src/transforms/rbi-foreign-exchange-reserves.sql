SELECT
    epoch_ms(timedate_ms)::DATE AS date,
    frequency,
    reserve_code,
    reserve_name,
    currency_code,
    CAST(amount AS DOUBLE) AS amount,
    fiscal_year
FROM "rbi-foreign-exchange-reserves"
WHERE timedate_ms IS NOT NULL
  AND amount IS NOT NULL
