-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "CD_SEX" AS cd_sex,
    "TX_SEX_DESCR_FR" AS tx_sex_descr_fr,
    "TX_SEX_DESCR_NL" AS tx_sex_descr_nl,
    "CD_AGE" AS cd_age,
    "TX_AGE_DESCR_FR" AS tx_age_descr_fr,
    "TX_AGE_DESCR_NL" AS tx_age_descr_nl,
    "CD_HST" AS cd_hst,
    "TX_HST_DESCR_FR" AS tx_hst_descr_fr,
    "TX_HST_DESCR_NL" AS tx_hst_descr_nl,
    "CD_CAS_LVL_1" AS cd_cas_lvl_1,
    "TX_CAS_DESCR_FR_LVL_1" AS tx_cas_descr_fr_lvl_1,
    "TX_CAS_DESCR_NL_LVL_1" AS tx_cas_descr_nl_lvl_1,
    "CD_CAS_LVL_2" AS cd_cas_lvl_2,
    "TX_CAS_DESCR_FR_LVL_2" AS tx_cas_descr_fr_lvl_2,
    "TX_CAS_DESCR_NL_LVL_2" AS tx_cas_descr_nl_lvl_2,
    "CD_EDU" AS cd_edu,
    "TX_EDU_DESCR_FR" AS tx_edu_descr_fr,
    "TX_EDU_DESCR_NL" AS tx_edu_descr_nl,
    CAST("MS_POP" AS BIGINT) AS ms_pop
FROM "statbel-nodeid5660"
