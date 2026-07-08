SELECT
    state,
    CAST(year AS INTEGER)          AS year,
    CAST(exports_usd_mn AS DOUBLE) AS exports_usd_mn
FROM "india-commerce-state-trade"
WHERE exports_usd_mn IS NOT NULL
