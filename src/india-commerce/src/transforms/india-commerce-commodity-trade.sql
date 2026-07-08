SELECT
    hs2_code,
    MIN(hs2_description)                                       AS hs2_description,
    CAST(year AS INTEGER)                                      AS year,
    SUM(value_usd_mn) FILTER (WHERE flow = 'Export')          AS exports_usd_mn,
    SUM(value_usd_mn) FILTER (WHERE flow = 'Import')          AS imports_usd_mn
FROM "india-commerce-commodity-trade"
GROUP BY hs2_code, year
HAVING SUM(value_usd_mn) IS NOT NULL
