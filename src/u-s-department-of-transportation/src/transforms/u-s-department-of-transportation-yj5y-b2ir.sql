-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "tbl",
    CAST("year" AS BIGINT) AS year,
    CAST("quarter" AS BIGINT) AS quarter,
    CAST("citymarketid_1" AS BIGINT) AS citymarketid_1,
    CAST("citymarketid_2" AS BIGINT) AS citymarketid_2,
    "city1",
    "city2",
    CAST("nsmiles" AS BIGINT) AS nsmiles,
    CAST("passengers" AS DOUBLE) AS passengers,
    CAST("fare" AS DOUBLE) AS fare,
    "carrier_lg",
    CAST("large_ms" AS DOUBLE) AS large_ms,
    CAST("fare_lg" AS DOUBLE) AS fare_lg,
    "carrier_low",
    CAST("lf_ms" AS DOUBLE) AS lf_ms,
    CAST("fare_low" AS DOUBLE) AS fare_low,
    CAST("table_1_flag" AS BIGINT) AS table_1_flag,
    "location_1",
    "location_1_address",
    "location_1_city",
    "location_1_state",
    "location_1_zip",
    "location_2",
    "location_2_address",
    "location_2_city",
    "location_2_state",
    "location_2_zip",
    CAST("tbl6pk" AS BIGINT) AS tbl6pk
FROM "u-s-department-of-transportation-yj5y-b2ir"
