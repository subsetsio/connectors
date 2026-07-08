SELECT
    CAST(year AS INTEGER)              AS year,
    CAST("Quarter" AS INTEGER)         AS quarter,
    "CategoryName_en"                  AS ship_type,
    "Port"                             AS direction,
    CAST(SUM(GREATEST(TRY_CAST("No" AS BIGINT), 0)) AS BIGINT) AS num_vessels,
    SUM(GREATEST(TRY_CAST("NetTonnage" AS DOUBLE), 0)) AS net_tonnage
FROM "suez-canal-authority-05-yealy-cargo-ton-by-region"
WHERE year IS NOT NULL AND "CategoryName_en" IS NOT NULL
GROUP BY 1, 2, 3, 4
