-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "msg_id",
    "tenant",
    CAST("intersection_id" AS BIGINT) AS intersection_id,
    "road_regulator_id",
    "intersection_name",
    CAST("min_tmstp_utc" AS TIMESTAMP) AS min_tmstp_utc,
    CAST("max_tmstp_utc" AS TIMESTAMP) AS max_tmstp_utc,
    "offset_tmstp_utc",
    CAST("moy_utc" AS BIGINT) AS moy_utc,
    CAST("layer_id" AS BIGINT) AS layer_id,
    "layer_type",
    CAST("msg_revision" AS BIGINT) AS msg_revision,
    CAST("elevation" AS BIGINT) AS elevation,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("intersection_revision" AS BIGINT) AS intersection_revision,
    CAST("lane_width" AS BIGINT) AS lane_width,
    "vehicle_max_speed",
    "vehicle_min_speed",
    "vehicle_night_max_speed",
    "max_speed_school_zone",
    "max_speed_school_zone_children",
    "max_speed_construction_zone",
    "truck_min_speed",
    "truck_max_speed",
    "truck_night_max_speed",
    "vehicle_trailer_min_speed",
    "vehicle_trailer_max_speed",
    "vehicle_trailer_night_max",
    "unknown_speed",
    "lane_set"
FROM "u-s-department-of-transportation-aj9z-iw7k"
