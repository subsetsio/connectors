-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "msg_id",
    "tenant",
    CAST("tmstp_utc" AS TIMESTAMP) AS tmstp_utc,
    CAST("date_utc" AS TIMESTAMP) AS date_utc,
    CAST("msg_moy_utc" AS BIGINT) AS msg_moy_utc,
    CAST("msg_milliseconds_utc" AS BIGINT) AS msg_milliseconds_utc,
    CAST("msg_count" AS BIGINT) AS msg_count,
    CAST("intersection_id" AS BIGINT) AS intersection_id,
    "road_regulator_id",
    "entity_id",
    CAST("station_id" AS BIGINT) AS station_id,
    CAST("msg_rank" AS BIGINT) AS msg_rank,
    CAST("requestor_name" AS BIGINT) AS requestor_name,
    "requestor_type",
    "vehicle_role",
    "vehicle_subrole",
    CAST("request_id" AS BIGINT) AS request_id,
    "request_type",
    CAST("request_duration" AS BIGINT) AS request_duration,
    CAST("request_moy_utc" AS BIGINT) AS request_moy_utc,
    CAST("request_milliseconds_utc" AS BIGINT) AS request_milliseconds_utc,
    CAST("inbound_lane" AS BIGINT) AS inbound_lane,
    CAST("heading" AS BIGINT) AS heading,
    CAST("elevation" AS BIGINT) AS elevation,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("speed" AS BIGINT) AS speed,
    "transmission"
FROM "u-s-department-of-transportation-p7d5-hrve"
