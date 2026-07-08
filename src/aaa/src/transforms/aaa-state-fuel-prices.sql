SELECT DISTINCT
    CAST(date AS DATE)        AS date,
    state_code,
    fuel_grade,
    CAST(price_usd AS DOUBLE) AS price_usd
FROM "aaa-state-fuel-prices"
WHERE price_usd > 0
