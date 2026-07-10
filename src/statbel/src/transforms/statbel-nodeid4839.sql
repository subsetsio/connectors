-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "CD_NACE" AS cd_nace,
    "TX_NACE_FR_LVL1" AS tx_nace_fr_lvl1,
    "TX_NACE_NL_LVL1" AS tx_nace_nl_lvl1,
    "TX_NACE_EN_LVL1" AS tx_nace_en_lvl1,
    "CD_RGN_REFNIS" AS cd_rgn_refnis,
    "TX_RGN_DESCR_FR" AS tx_rgn_descr_fr,
    "TX_RGN_DESCR_NL" AS tx_rgn_descr_nl,
    "TX_RGN_DESCR_EN" AS tx_rgn_descr_en,
    "CD_GENDER" AS cd_gender,
    "TX_GENDER_DESCR_FR" AS tx_gender_descr_fr,
    "TX_GENDER_DESCR_NL" AS tx_gender_descr_nl,
    "TX_GENDER_DESCR_EN" AS tx_gender_descr_en,
    CAST("CD_AGE_RANGE" AS BIGINT) AS cd_age_range,
    "AGE_RANGE_DESCR_FR" AS age_range_descr_fr,
    "AGE_RANGE_DESCR_NL" AS age_range_descr_nl,
    "AGE_RANGE_DESCR_EN" AS age_range_descr_en,
    CAST("MS_ENTREP_NUM" AS BIGINT) AS ms_entrep_num
FROM "statbel-nodeid4839"
