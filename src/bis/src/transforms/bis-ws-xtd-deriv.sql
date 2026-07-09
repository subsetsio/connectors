-- WS_XTD_DERIV: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "od_type",
    "od_type_label",
    "od_risk_cat",
    "od_risk_cat_label",
    "od_instr",
    "od_instr_label",
    "issue_cur",
    "issue_cur_label",
    "xd_exchange",
    "xd_exchange_label",
    "time_period",
    "period_start",
    "obs_value",
    "collection",
    "availability",
    "decimals",
    "bis_unit",
    "unit_mult",
    "obs_status",
    "obs_conf",
    "obs_pre_break"
FROM "bis-ws-xtd-deriv"
WHERE obs_value IS NOT NULL
