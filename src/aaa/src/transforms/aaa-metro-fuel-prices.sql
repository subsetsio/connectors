SELECT DISTINCT
    CAST(date AS DATE)        AS date,
    state_code,
    metro_area,
    fuel_grade,
    CAST(price_usd AS DOUBLE) AS price_usd
FROM "aaa-metro-fuel-prices"
WHERE price_usd > 0
