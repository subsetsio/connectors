-- WS_CPMI_PARTICIP: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "rep_cty",
    "rep_cty_label",
    "system_type",
    "system_type_label",
    "system",
    "system_label",
    "part_type",
    "part_type_label",
    "time_period",
    "period_start",
    "obs_value",
    "unit_mult",
    "unit_measure",
    "title",
    "table",
    "decimals",
    "comment_ts",
    "availability",
    "time_format",
    "collection",
    "old_table",
    "obs_status",
    "obs_pre_break",
    "obs_conf",
    "comment_obs"
FROM "bis-ws-cpmi-particip"
WHERE obs_value IS NOT NULL
