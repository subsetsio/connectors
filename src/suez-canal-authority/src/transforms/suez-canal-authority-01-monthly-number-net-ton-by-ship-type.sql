SELECT
    make_date(CAST(year AS INTEGER), CAST("Month" AS INTEGER), 1) AS date,
    CAST(year AS INTEGER)              AS year,
    CAST("Month" AS INTEGER)           AS month,
    "Ship Type"                        AS ship_type,
    "Direction"                        AS direction,
    "State"                            AS cargo_state,
    CAST(SUM(GREATEST(TRY_CAST("No" AS BIGINT), 0)) AS BIGINT) AS num_vessels,
    SUM(GREATEST(TRY_CAST("NetTonnage" AS DOUBLE), 0)) AS net_tonnage
FROM "suez-canal-authority-01-monthly-number-net-ton-by-ship-type"
WHERE year IS NOT NULL AND "Ship Type" IS NOT NULL
GROUP BY 1, 2, 3, 4, 5, 6
