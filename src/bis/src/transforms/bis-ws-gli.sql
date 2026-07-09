-- WS_GLI: one row per (series_key, time_period) observation.
-- Raw already carries typed obs_value / period_start and split code+label
-- dimension columns, so this is a projection plus the missing-observation gate.
SELECT
    "series_key",
    "freq",
    "freq_label",
    "curr_denom",
    "curr_denom_label",
    "borrowers_cty",
    "borrowers_cty_label",
    "borrowers_sector",
    "borrowers_sector_label",
    "lenders_sector",
    "lenders_sector_label",
    "l_pos_type",
    "l_pos_type_label",
    "l_instr",
    "l_instr_label",
    "unit_measure",
    "unit_measure_label",
    "time_period",
    "period_start",
    "obs_value",
    "title",
    "unit_mult",
    "decimals",
    "collection",
    "availability",
    "obs_status",
    "obs_pre_break",
    "obs_conf"
FROM "bis-ws-gli"
WHERE obs_value IS NOT NULL
