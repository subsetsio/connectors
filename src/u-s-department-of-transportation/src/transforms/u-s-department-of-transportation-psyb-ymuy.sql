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
    "signal_moy_utc",
    "signal_milliseconds_utc",
    CAST("request_id" AS BIGINT) AS request_id,
    "status",
    "vehicle_role",
    CAST("signal_msg_count" AS BIGINT) AS signal_msg_count,
    "duration",
    CAST("inbound_lane" AS BIGINT) AS inbound_lane,
    CAST("status_msg_count" AS BIGINT) AS status_msg_count
FROM "u-s-department-of-transportation-psyb-ymuy"
