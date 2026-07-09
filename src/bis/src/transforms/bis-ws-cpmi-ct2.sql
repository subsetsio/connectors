-- WS_CPMI_CT2: one row per (series_key, time_period) observation.
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
    "indicator_ct",
    "indicator_ct_label",
    "measure",
    "measure_label",
    "unit_measure",
    "unit_measure_label",
    "time_period",
    "period_start",
    "obs_value",
    "unit_mult",
    "table",
    "title_ts",
    "decimals",
    "collection",
    "availability",
    "time_format",
    "obs_pre_break",
    "obs_conf",
    "obs_status"
FROM "bis-ws-cpmi-ct2"
WHERE obs_value IS NOT NULL
