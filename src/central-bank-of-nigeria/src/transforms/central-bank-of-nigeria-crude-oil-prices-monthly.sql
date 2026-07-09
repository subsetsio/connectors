-- the source's `period` label ("May 2026") is dropped: it restates year+month
-- `id` is dropped: (year, month) is the source's real grain and is unique
SELECT
    CAST("period_start_iso" AS DATE) AS month_start,
    CAST("tyear" AS BIGINT) AS year,
    CAST("tmonth" AS BIGINT) AS month,
    TRY_CAST(NULLIF(TRIM("crudeOilPrice"), '') AS DOUBLE) AS crude_oil_price,
    TRY_CAST(NULLIF(TRIM("domProd"), '') AS DOUBLE) AS domestic_production,
    TRY_CAST(NULLIF(TRIM("crudeOilExp"), '') AS DOUBLE) AS crude_oil_exports
FROM "central-bank-of-nigeria-crude-oil-prices-monthly"
