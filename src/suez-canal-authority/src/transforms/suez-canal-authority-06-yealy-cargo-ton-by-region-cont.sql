SELECT
    CAST(year AS INTEGER)                  AS year,
    "Region"                               AS region,
    "Region_Code"                          AS region_code,
    "Direction"                            AS direction,
    "Terminal"                             AS terminal,
    SUM(GREATEST(TRY_CAST("CargoTonnage" AS DOUBLE), 0)) AS cargo_tonnage
FROM "suez-canal-authority-06-yealy-cargo-ton-by-region-cont"
WHERE year IS NOT NULL AND "Region" IS NOT NULL
GROUP BY 1, 2, 3, 4, 5
