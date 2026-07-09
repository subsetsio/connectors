-- WS_TC: one row per (series_key, time_period) observation.
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
    "valuation",
    "valuation_label",
    "unit_type",
    "unit_type_label",
    "tc_adjust",
    "tc_adjust_label",
    "time_period",
    "period_start",
    "obs_value",
    "collection",
    "unit_mult",
    "unit_measure",
    "title_ts",
    "decimals",
    "obs_status",
    "obs_pre_break",
    "obs_conf"
FROM "bis-ws-tc"
WHERE obs_value IS NOT NULL
