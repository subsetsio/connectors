-- WS_CPMI_MACRO: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "bis_topic",
    "bis_topic_label",
    "rep_cty",
    "rep_cty_label",
    "bis_suffix",
    "bis_suffix_label",
    "time_period",
    "period_start",
    "obs_value",
    "comment_ts",
    "collection",
    "time_format",
    "availability",
    "bis_unit",
    "decimals",
    "title",
    "unit_mult",
    "obs_conf",
    "obs_status",
    "obs_pre_break"
FROM "bis-ws-cpmi-macro"
WHERE obs_value IS NOT NULL
