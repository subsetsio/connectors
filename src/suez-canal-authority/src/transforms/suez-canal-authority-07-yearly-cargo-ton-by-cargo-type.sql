SELECT
    CAST("Year" AS INTEGER)                AS year,
    "CargoType"                            AS cargo_type,
    "Goods"                                AS cargo_group,
    "Direction"                            AS direction,
    SUM(GREATEST(TRY_CAST("CargoTonnage" AS DOUBLE), 0)) AS cargo_tonnage
FROM "suez-canal-authority-07-yearly-cargo-ton-by-cargo-type"
WHERE "Year" IS NOT NULL AND "CargoType" IS NOT NULL
GROUP BY 1, 2, 3, 4
