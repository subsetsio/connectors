-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tmc",
    "road",
    "direction",
    "intersection",
    "state",
    "county",
    CAST("zip" AS BIGINT) AS zip,
    CAST("start_latitude" AS DOUBLE) AS start_latitude,
    CAST("start_longitude" AS DOUBLE) AS start_longitude,
    CAST("end_latitude" AS DOUBLE) AS end_latitude,
    CAST("end_longitude" AS DOUBLE) AS end_longitude,
    CAST("miles" AS DOUBLE) AS miles,
    CAST("road_order" AS DOUBLE) AS road_order,
    "timezone_name",
    "type",
    "country",
    CAST("active_start_date" AS TIMESTAMP) AS active_start_date,
    "active_end_date"
FROM "u-s-department-of-transportation-5zqs-rgz5"
