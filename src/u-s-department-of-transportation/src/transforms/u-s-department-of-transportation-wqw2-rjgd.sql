-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tbl",
    CAST("year" AS BIGINT) AS year,
    CAST("quarter" AS BIGINT) AS quarter,
    CAST("citymarketid" AS BIGINT) AS citymarketid,
    "city",
    CAST("markets" AS BIGINT) AS markets,
    CAST("cur_passengers" AS BIGINT) AS cur_passengers,
    CAST("cur_fare" AS DOUBLE) AS cur_fare,
    CAST("cur_yield" AS DOUBLE) AS cur_yield,
    CAST("distance" AS DOUBLE) AS distance,
    CAST("ly_passengers" AS BIGINT) AS ly_passengers,
    CAST("ly_fare" AS DOUBLE) AS ly_fare,
    CAST("ly_yield" AS DOUBLE) AS ly_yield,
    CAST("ly_distance" AS DOUBLE) AS ly_distance,
    "location_1",
    "location_1_address",
    "location_1_city",
    "location_1_state",
    "location_1_zip",
    CAST("unique_id" AS BIGINT) AS unique_id
FROM "u-s-department-of-transportation-wqw2-rjgd"
