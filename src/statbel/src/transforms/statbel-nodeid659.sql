-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "CD_GEO_LVL_0" AS cd_geo_lvl_0,
    "CD_GEO_LVL_1" AS cd_geo_lvl_1,
    "TX_GEO_DESCR_FR_LVL_1" AS tx_geo_descr_fr_lvl_1,
    "TX_GEO_DESCR_NL_LVL_1" AS tx_geo_descr_nl_lvl_1,
    "CD_GEO_LVL_2" AS cd_geo_lvl_2,
    "TX_GEO_DESCR_FR_LVL_2" AS tx_geo_descr_fr_lvl_2,
    "TX_GEO_DESCR_NL_LVL_2" AS tx_geo_descr_nl_lvl_2,
    "CD_GEO_LVL_3" AS cd_geo_lvl_3,
    "TX_GEO_DESCR_FR_LVL_3" AS tx_geo_descr_fr_lvl_3,
    "TX_GEO_DESCR_NL_LVL_3" AS tx_geo_descr_nl_lvl_3,
    "CD_TFN_LVL_0" AS cd_tfn_lvl_0,
    "CD_TFN_LVL_1" AS cd_tfn_lvl_1,
    "TX_TFN_DESCR_FR_LVL_1" AS tx_tfn_descr_fr_lvl_1,
    "TX_TFN_DESCR_NL_LVL_1" AS tx_tfn_descr_nl_lvl_1,
    "CD_TFN_LVL_2" AS cd_tfn_lvl_2,
    "TX_TFN_DESCR_FR_LVL_2" AS tx_tfn_descr_fr_lvl_2,
    "TX_TFN_DESCR_NL_LVL_2" AS tx_tfn_descr_nl_lvl_2,
    "CD_TFN_LVL_3" AS cd_tfn_lvl_3,
    "TX_TFN_DESCR_FR_LVL_3" AS tx_tfn_descr_fr_lvl_3,
    "TX_TFN_DESCR_NL_LVL_3" AS tx_tfn_descr_nl_lvl_3,
    "CD_SFN_LVL_0" AS cd_sfn_lvl_0,
    "CD_SFN_LVL_1" AS cd_sfn_lvl_1,
    "TX_SFN_DESCR_FR_LVL_1" AS tx_sfn_descr_fr_lvl_1,
    "TX_SFN_DESCR_NL_LVL_1" AS tx_sfn_descr_nl_lvl_1,
    "CD_SFN_LVL_2" AS cd_sfn_lvl_2,
    "TX_SFN_DESCR_FR_LVL_2" AS tx_sfn_descr_fr_lvl_2,
    "TX_SFN_DESCR_NL_LVL_2" AS tx_sfn_descr_nl_lvl_2,
    "CD_SFN_LVL_3" AS cd_sfn_lvl_3,
    "TX_SFN_DESCR_FR_LVL_3" AS tx_sfn_descr_fr_lvl_3,
    "TX_SFN_DESCR_NL_LVL_3" AS tx_sfn_descr_nl_lvl_3,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "statbel-nodeid659"
