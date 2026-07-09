-- WS_CPMI_DEVICES: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "rep_cty",
    "rep_cty_label",
    "device_type",
    "device_type_label",
    "function",
    "function_label",
    "sub_function",
    "sub_function_label",
    "technology",
    "technology_label",
    "issuer",
    "issuer_label",
    "time_period",
    "period_start",
    "obs_value",
    "unit_mult",
    "unit_measure",
    "title",
    "decimals",
    "collection",
    "availability",
    "table",
    "comment_ts",
    "time_format",
    "old_table",
    "obs_status",
    "obs_pre_break",
    "obs_conf",
    "comment_obs"
FROM "bis-ws-cpmi-devices"
WHERE obs_value IS NOT NULL
