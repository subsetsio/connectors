-- WS_DSR: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "borrowers_cty",
    "borrowers_cty_label",
    "dsr_borrowers",
    "dsr_borrowers_label",
    "time_period",
    "period_start",
    "obs_value",
    "collection",
    "unit_measure",
    "unit_mult",
    "decimals",
    "title_ts",
    "obs_conf",
    "obs_pre_break",
    "obs_status"
FROM "bis-ws-dsr"
WHERE obs_value IS NOT NULL
