-- WS_CPMI_INSTITUT: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "rep_cty",
    "rep_cty_label",
    "institution_type",
    "institution_type_label",
    "measure",
    "measure_label",
    "indicator",
    "indicator_label",
    "time_period",
    "period_start",
    "obs_value",
    "time_format",
    "availability",
    "collection",
    "comment_ts",
    "decimals",
    "table",
    "title",
    "unit_measure",
    "unit_mult",
    "old_table",
    "obs_status",
    "obs_conf",
    "obs_pre_break",
    "comment_obs"
FROM "bis-ws-cpmi-institut"
WHERE obs_value IS NOT NULL
