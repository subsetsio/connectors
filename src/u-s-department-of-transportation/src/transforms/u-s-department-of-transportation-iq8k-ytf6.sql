-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "msg_id",
    "tenant",
    CAST("tmstp_utc" AS TIMESTAMP) AS tmstp_utc,
    CAST("date_utc" AS TIMESTAMP) AS date_utc,
    CAST("intersection_id" AS BIGINT) AS intersection_id,
    "road_regulator_id",
    "intersection_name",
    CAST("msg_moy_utc" AS BIGINT) AS msg_moy_utc,
    CAST("intersection_moy_utc" AS BIGINT) AS intersection_moy_utc,
    CAST("intersection_milliseconds" AS BIGINT) AS intersection_milliseconds,
    CAST("intersection_msg_count" AS BIGINT) AS intersection_msg_count,
    CAST("intersection_status_flags" AS BIGINT) AS intersection_status_flags,
    CAST("manual_control_enabled" AS BOOLEAN) AS manual_control_enabled,
    CAST("stop_time_activated" AS BOOLEAN) AS stop_time_activated,
    CAST("failure_flash" AS BOOLEAN) AS failure_flash,
    CAST("preempt_active" AS BOOLEAN) AS preempt_active,
    CAST("signal_priority_active" AS BOOLEAN) AS signal_priority_active,
    CAST("fixed_time_operation" AS BOOLEAN) AS fixed_time_operation,
    CAST("traffic_dependent_operation" AS BOOLEAN) AS traffic_dependent_operation,
    CAST("standby_operation" AS BOOLEAN) AS standby_operation,
    CAST("failure_mode" AS BOOLEAN) AS failure_mode,
    CAST("controller_off" AS BOOLEAN) AS controller_off,
    CAST("recent_map_message_update" AS BOOLEAN) AS recent_map_message_update,
    CAST("recent_change_in_map_assigned" AS BOOLEAN) AS recent_change_in_map_assigned,
    CAST("no_valid_map_is_available" AS BOOLEAN) AS no_valid_map_is_available,
    CAST("no_valid_spat_is_available" AS BOOLEAN) AS no_valid_spat_is_available,
    CAST("reserved_bits_1" AS BOOLEAN) AS reserved_bits_1,
    CAST("reserved_bits_2" AS BOOLEAN) AS reserved_bits_2,
    "intersection_states"
FROM "u-s-department-of-transportation-iq8k-ytf6"
