-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "CD_REFNIS_LVL_1" AS cd_refnis_lvl_1,
    "CD_REFNIS_LVL_2" AS cd_refnis_lvl_2,
    "TX_REFNIS_DESCR_FR_LVL_2" AS tx_refnis_descr_fr_lvl_2,
    "TX_REFNIS_DESCR_NL_LVL_2" AS tx_refnis_descr_nl_lvl_2,
    "CD_SEX" AS cd_sex,
    "TX_SEX_DESCR_FR" AS tx_sex_descr_fr,
    "TX_SEX_DESCR_NL" AS tx_sex_descr_nl,
    "CD_AGE" AS cd_age,
    "TX_AGE_DESCR_FR" AS tx_age_descr_fr,
    "TX_AGE_DESCR_NL" AS tx_age_descr_nl,
    "CD_FST" AS cd_fst,
    "TX_FST_DESCR_FR" AS tx_fst_descr_fr,
    "TX_FST_DESCR_NL" AS tx_fst_descr_nl,
    "CD_SIE" AS cd_sie,
    "TX_SIE_DESCR_FR" AS tx_sie_descr_fr,
    "TX_SIE_DESCR_NL" AS tx_sie_descr_nl,
    "CD_POB_LVL_1" AS cd_pob_lvl_1,
    "TX_POB_DESCR_FR_LVL_1" AS tx_pob_descr_fr_lvl_1,
    "TX_POB_DESCR_NL_LVL_1" AS tx_pob_descr_nl_lvl_1,
    "CD_POB_LVL_2" AS cd_pob_lvl_2,
    "TX_POB_DESCR_FR_LVL_2" AS tx_pob_descr_fr_lvl_2,
    "TX_POB_DESCR_NL_LVL_2" AS tx_pob_descr_nl_lvl_2,
    CAST("MS_POP" AS BIGINT) AS ms_pop
FROM "statbel-nodeid5683"
