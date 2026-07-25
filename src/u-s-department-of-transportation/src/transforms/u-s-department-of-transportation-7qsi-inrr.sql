-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("zone_id" AS BIGINT) AS zone_id,
    "display_name",
    "state",
    "rtmc",
    "timezone",
    "road",
    "direction",
    "location_description",
    "lane_type",
    "organization",
    "detector_type",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    "bearing",
    "default_speed",
    "interval",
    "length"
FROM "u-s-department-of-transportation-7qsi-inrr"
