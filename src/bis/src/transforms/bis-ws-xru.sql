-- WS_XRU: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "ref_area",
    "ref_area_label",
    "currency",
    "currency_label",
    "collection",
    "collection_label",
    "time_period",
    "period_start",
    "obs_value",
    "unit_mult",
    "decimals",
    "availability",
    "title",
    "obs_status",
    "obs_pre_break",
    "obs_conf"
FROM "bis-ws-xru"
WHERE obs_value IS NOT NULL
