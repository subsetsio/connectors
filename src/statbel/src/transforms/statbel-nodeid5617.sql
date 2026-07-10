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
    "CD_LPW_LVL_1" AS cd_lpw_lvl_1,
    "CD_LPW_LVL_2" AS cd_lpw_lvl_2,
    "CD_LPW_LVL_3" AS cd_lpw_lvl_3,
    "TX_LPW_DESCR_FR_LVL_3" AS tx_lpw_descr_fr_lvl_3,
    "TX_LPW_DESCR_NL_LVL_3" AS tx_lpw_descr_nl_lvl_3,
    "CD_IND" AS cd_ind,
    "TX_IND_DESCR_FR" AS tx_ind_descr_fr,
    "TX_IND_DESCR_NL" AS tx_ind_descr_nl,
    CAST("MS_POP" AS BIGINT) AS ms_pop
FROM "statbel-nodeid5617"
