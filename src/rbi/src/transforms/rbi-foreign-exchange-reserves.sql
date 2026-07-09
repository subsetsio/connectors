SELECT
    CAST(observation_date AS DATE) AS date,
    frequency,
    reserve_code,
    reserve_name,
    currency_code,
    CAST(amount AS DOUBLE) AS amount,
    fiscal_year
FROM "rbi-foreign-exchange-reserves"
WHERE observation_date IS NOT NULL
  AND amount IS NOT NULL
