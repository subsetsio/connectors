-- WS_LONG_CPI: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "ref_area",
    "ref_area_label",
    "unit_measure",
    "unit_measure_label",
    "time_period",
    "period_start",
    "obs_value",
    "unit_mult",
    "time_format",
    "breaks",
    "coverage",
    "decimals",
    "title_ts",
    "obs_conf",
    "obs_pre_break",
    "obs_status"
FROM "bis-ws-long-cpi"
WHERE obs_value IS NOT NULL
