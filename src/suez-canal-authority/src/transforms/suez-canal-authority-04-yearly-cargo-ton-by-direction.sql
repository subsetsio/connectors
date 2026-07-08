SELECT
    CAST("Year" AS INTEGER)         AS year,
    "Direction"                     AS direction,
    TRY_CAST("Cargo Ton" AS DOUBLE) AS cargo_ton
FROM "suez-canal-authority-04-yearly-cargo-ton-by-direction"
WHERE "Year" IS NOT NULL
