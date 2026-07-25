-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "tmc_code",
    CAST("measurement_tstamp" AS TIMESTAMP) AS measurement_tstamp,
    CAST("speed" AS DOUBLE) AS speed,
    CAST("average_speed" AS DOUBLE) AS average_speed,
    CAST("reference_speed" AS DOUBLE) AS reference_speed,
    CAST("travel_time_minutes" AS DOUBLE) AS travel_time_minutes,
    CAST("confidence_score" AS DOUBLE) AS confidence_score,
    CAST("cvalue" AS DOUBLE) AS cvalue,
    CAST("start_time" AS TIMESTAMP) AS start_time,
    CAST("end_time" AS TIMESTAMP) AS end_time,
    CAST("time_start_record" AS TIMESTAMP) AS time_start_record,
    CAST("time_end_record" AS TIMESTAMP) AS time_end_record,
    "id",
    CAST("order" AS BIGINT) AS order,
    CAST("miles" AS DOUBLE) AS miles,
    "direction",
    CAST("distance_to_work_zone" AS DOUBLE) AS distance_to_work_zone,
    CAST("distance_e_to_wz" AS DOUBLE) AS distance_e_to_wz,
    CAST("sholder_closure_count" AS DOUBLE) AS sholder_closure_count,
    CAST("traffic_lane_closure_count" AS DOUBLE) AS traffic_lane_closure_count,
    "week",
    CAST("volume" AS DOUBLE) AS volume,
    CAST("max_lanes_closed" AS DOUBLE) AS max_lanes_closed,
    "road_name",
    "road_type",
    CAST("on_ramp" AS BIGINT) AS on_ramp,
    CAST("off_ramp" AS BIGINT) AS off_ramp,
    "incident_id",
    "description",
    CAST("lanes" AS BIGINT) AS lanes
FROM "u-s-department-of-transportation-ag7u-9n3t"
