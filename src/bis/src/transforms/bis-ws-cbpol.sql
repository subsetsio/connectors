-- WS_CBPOL: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "ref_area",
    "ref_area_label",
    "time_period",
    "period_start",
    "obs_value",
    "unit_measure",
    "unit_mult",
    "time_format",
    "compilation",
    "decimals",
    "source_ref",
    "supp_info_breaks",
    "title",
    "obs_status",
    "obs_conf",
    "obs_pre_break"
FROM "bis-ws-cbpol"
WHERE obs_value IS NOT NULL
