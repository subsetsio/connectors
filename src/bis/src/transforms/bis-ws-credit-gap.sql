-- WS_CREDIT_GAP: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "borrowers_cty",
    "borrowers_cty_label",
    "tc_borrowers",
    "tc_borrowers_label",
    "tc_lenders",
    "tc_lenders_label",
    "cg_dtype",
    "cg_dtype_label",
    "time_period",
    "period_start",
    "obs_value",
    "collection",
    "decimals",
    "unit_measure",
    "unit_mult",
    "time_format",
    "title_ts",
    "obs_status",
    "obs_conf",
    "obs_pre_break"
FROM "bis-ws-credit-gap"
WHERE obs_value IS NOT NULL
