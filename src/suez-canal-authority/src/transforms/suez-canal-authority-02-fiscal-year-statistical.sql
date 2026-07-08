SELECT
    "Fiscal Year"                          AS fiscal_year,
    TRY_CAST("No ( Vessel )" AS BIGINT)    AS num_vessels,
    TRY_CAST("Net Ton" AS DOUBLE)          AS net_ton,
    TRY_CAST("Cargo Ton" AS DOUBLE)        AS cargo_ton,
    TRY_CAST("Tolls (Million $ )" AS DOUBLE)     AS tolls_million_usd,
    TRY_CAST("Tolls (Million L.E. )" AS DOUBLE)  AS tolls_million_egp
FROM "suez-canal-authority-02-fiscal-year-statistical"
WHERE "Fiscal Year" IS NOT NULL
