-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("feed_update_date" AS TIMESTAMP) AS feed_update_date,
    CAST("road_event_feed_info_version" AS DOUBLE) AS road_event_feed_info_version,
    "road_event_id",
    "subidentifier",
    "road_name",
    "road_number",
    "direction",
    "beginning_cross_street",
    "ending_cross_street",
    "beginning_milepost",
    "ending_milepost",
    "beginning_accuracy",
    "ending_accuracy",
    CAST("start_date" AS TIMESTAMP) AS start_date,
    CAST("end_date" AS TIMESTAMP) AS end_date,
    "start_date_accuracy",
    "end_date_accuracy",
    "event_status",
    CAST("total_num_lanes" AS DOUBLE) AS total_num_lanes,
    "vehicle_impact",
    "workers_present",
    "reduced_speed_limit",
    "restrictions",
    "description",
    "issuing_organization",
    "creation_date",
    "update_date",
    "types_of_work",
    "lanes",
    "geometry_linestring",
    "geometry_multipoint"
FROM "u-s-department-of-transportation-h4kh-i7b7"
