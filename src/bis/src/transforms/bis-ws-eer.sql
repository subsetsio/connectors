-- WS_EER: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "eer_type",
    "eer_type_label",
    "eer_basket",
    "eer_basket_label",
    "ref_area",
    "ref_area_label",
    "time_period",
    "period_start",
    "obs_value",
    "time_format",
    "collection",
    "title_ts",
    "unit_measure",
    "obs_status",
    "obs_conf",
    "obs_pre_break"
FROM "bis-ws-eer"
WHERE obs_value IS NOT NULL
