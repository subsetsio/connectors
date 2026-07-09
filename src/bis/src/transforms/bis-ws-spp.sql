-- WS_SPP: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "ref_area",
    "ref_area_label",
    "value",
    "value_label",
    "unit_measure",
    "unit_measure_label",
    "time_period",
    "period_start",
    "obs_value",
    "unit_mult",
    "breaks",
    "coverage",
    "title_ts",
    "obs_status",
    "obs_conf",
    "obs_pre_break"
FROM "bis-ws-spp"
WHERE obs_value IS NOT NULL
