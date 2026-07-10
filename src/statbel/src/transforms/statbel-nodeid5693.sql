-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "CD_REFNIS_LVL_1" AS cd_refnis_lvl_1,
    "CD_REFNIS_LVL_2" AS cd_refnis_lvl_2,
    CAST("CD_REFNIS_LVL_3" AS BIGINT) AS cd_refnis_lvl_3,
    CAST("CD_REFNIS_LVL_4" AS BIGINT) AS cd_refnis_lvl_4,
    "TX_REFNIS_DESCR_FR_LVL_4" AS tx_refnis_descr_fr_lvl_4,
    "TX_REFNIS_DESCR_NL_LVL_4" AS tx_refnis_descr_nl_lvl_4,
    "CD_TOB_LVL_1" AS cd_tob_lvl_1,
    "TX_TOB_DESCR_FR_LVL_1" AS tx_tob_descr_fr_lvl_1,
    "TX_TOB_DESCR_NL_LVL_1" AS tx_tob_descr_nl_lvl_1,
    "CD_TOB_LVL_2" AS cd_tob_lvl_2,
    "TX_TOB_DESCR_FR_LVL_2" AS tx_tob_descr_fr_lvl_2,
    "TX_TOB_DESCR_NL_LVL_2" AS tx_tob_descr_nl_lvl_2,
    "CD_OCS" AS cd_ocs,
    "TX_OCS_DESCR_FR" AS tx_ocs_descr_fr,
    "TX_OCS_DESCR_NL" AS tx_ocs_descr_nl,
    CAST("MS_LOGEMENTS" AS BIGINT) AS ms_logements
FROM "statbel-nodeid5693"
