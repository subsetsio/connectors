-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "CD_FREQ" AS cd_freq,
    "CD_REF_AREA" AS cd_ref_area,
    "CD_SEASONAL_ADJUST" AS cd_seasonal_adjust,
    "TX_SEASONAL_ADJUST_DESCR_FR" AS tx_seasonal_adjust_descr_fr,
    "TX_SEASONAL_ADJUST_DESCR_NL" AS tx_seasonal_adjust_descr_nl,
    "TX_SEASONAL_ADJUST_DESCR_EN" AS tx_seasonal_adjust_descr_en,
    "CD_INDICATOR" AS cd_indicator,
    "TX_INDICATOR_DESCR_FR" AS tx_indicator_descr_fr,
    "TX_INDICATOR_DESCR_NL" AS tx_indicator_descr_nl,
    "TX_INDICATOR_DESCR_EN" AS tx_indicator_descr_en,
    "CD_ACTIVITY" AS cd_activity,
    "TX_ACTIVITY_DESCR_FR" AS tx_activity_descr_fr,
    "TX_ACTIVITY_DESCR_NL" AS tx_activity_descr_nl,
    "TX_ACTIVITY_DESCR_EN" AS tx_activity_descr_en,
    CAST("CD_BASE_PER" AS BIGINT) AS cd_base_per,
    strptime("DT_TIME_PERIOD", '%Y-%m')::DATE AS dt_time_period,
    CAST("MS_OBS_VALUE" AS DOUBLE) AS ms_obs_value
FROM "statbel-nodeid5726"
