SELECT
    CAST("Year" AS INTEGER)                AS year,
    TRY_CAST("No ( Vessel )" AS BIGINT)    AS num_vessels,
    TRY_CAST("Net Ton" AS DOUBLE)          AS net_ton,
    TRY_CAST("Cargo Ton" AS DOUBLE)        AS cargo_ton,
    TRY_CAST("Tolls (Million $ )" AS DOUBLE)     AS tolls_million_usd,
    TRY_CAST("Tolls (Million L.E. )" AS DOUBLE)  AS tolls_million_egp
FROM "suez-canal-authority-03-yearly-statistics"
WHERE "Year" IS NOT NULL
