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
    "CD_TOB_LVL_0" AS cd_tob_lvl_0,
    "CD_TOB_LVL_1" AS cd_tob_lvl_1,
    "TX_TOB_DESCR_FR_LVL_1" AS tx_tob_descr_fr_lvl_1,
    "TX_TOB_DESCR_NL_LVL_1" AS tx_tob_descr_nl_lvl_1,
    "CD_TOB_LVL_2" AS cd_tob_lvl_2,
    "TX_TOB_DESCR_FR_LVL_2" AS tx_tob_descr_fr_lvl_2,
    "TX_TOB_DESCR_NL_LVL_2" AS tx_tob_descr_nl_lvl_2,
    "CD_OCS_LVL_0" AS cd_ocs_lvl_0,
    "CD_OCS_LVL_1" AS cd_ocs_lvl_1,
    "TX_OCS_DESCR_FR_LVL_1" AS tx_ocs_descr_fr_lvl_1,
    "TX_OCS_DESCR_NL_LVL_1" AS tx_ocs_descr_nl_lvl_1,
    "CD_POC_LVL_0" AS cd_poc_lvl_0,
    "CD_POC_LVL_1" AS cd_poc_lvl_1,
    "TX_POC_DESCR_FR_LVL_1" AS tx_poc_descr_fr_lvl_1,
    "TX_POC_DESCR_NL_LVL_1" AS tx_poc_descr_nl_lvl_1,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "statbel-nodeid662"
