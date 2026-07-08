SELECT DISTINCT
    CAST(date AS DATE)        AS date,
    fuel_grade,
    CAST(price_usd AS DOUBLE) AS price_usd
FROM "aaa-national-fuel-prices"
WHERE price_usd > 0
