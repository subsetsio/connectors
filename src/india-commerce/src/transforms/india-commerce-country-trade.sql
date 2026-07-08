SELECT
    country_code,
    country_name,
    CAST(year AS INTEGER)                AS year,
    CAST(exports_usd_mn AS DOUBLE)       AS exports_usd_mn,
    CAST(imports_usd_mn AS DOUBLE)       AS imports_usd_mn,
    CAST(trade_balance_usd_mn AS DOUBLE) AS trade_balance_usd_mn
FROM "india-commerce-country-trade"
WHERE exports_usd_mn IS NOT NULL OR imports_usd_mn IS NOT NULL
