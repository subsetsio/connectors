SELECT
  CAST(date AS DATE) AS date,
  TRY_CAST(exchange_rate_usd AS DOUBLE) AS exchange_rate_usd
FROM "mas-d-046ff8d521a218d9178178cfbfc45c2c"
WHERE date IS NOT NULL
  AND TRY_CAST(exchange_rate_usd AS DOUBLE) IS NOT NULL
