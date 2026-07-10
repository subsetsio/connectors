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
    "CD_SEX_LVL_0" AS cd_sex_lvl_0,
    "CD_SEX_LVL_1" AS cd_sex_lvl_1,
    "TX_SEX_DESCR_FR_LVL_1" AS tx_sex_descr_fr_lvl_1,
    "TX_SEX_DESCR_NL_LVL_1" AS tx_sex_descr_nl_lvl_1,
    "CD_IND_LVL_0" AS cd_ind_lvl_0,
    "CD_IND_LVL_1" AS cd_ind_lvl_1,
    "TX_IND_DESCR_FR_LVL_1" AS tx_ind_descr_fr_lvl_1,
    "TX_IND_DESCR_NL_LVL_1" AS tx_ind_descr_nl_lvl_1,
    "CD_IND_LVL_2" AS cd_ind_lvl_2,
    "TX_IND_DESCR_FR_LVL_2" AS tx_ind_descr_fr_lvl_2,
    "TX_IND_DESCR_NL_LVL_2" AS tx_ind_descr_nl_lvl_2,
    "CD_CAS_LVL_0" AS cd_cas_lvl_0,
    "CD_CAS_LVL_1" AS cd_cas_lvl_1,
    "TX_CAS_DESCR_FR_LVL_1" AS tx_cas_descr_fr_lvl_1,
    "TX_CAS_DESCR_NL_LVL_1" AS tx_cas_descr_nl_lvl_1,
    "CD_CAS_LVL_2" AS cd_cas_lvl_2,
    "TX_CAS_DESCR_FR_LVL_2" AS tx_cas_descr_fr_lvl_2,
    "TX_CAS_DESCR_NL_LVL_2" AS tx_cas_descr_nl_lvl_2,
    "CD_CAS_LVL_3" AS cd_cas_lvl_3,
    "TX_CAS_DESCR_FR_LVL_3" AS tx_cas_descr_fr_lvl_3,
    "TX_CAS_DESCR_NL_LVL_3" AS tx_cas_descr_nl_lvl_3,
    "CD_EDU_LVL_0" AS cd_edu_lvl_0,
    "CD_EDU_LVL_1" AS cd_edu_lvl_1,
    "TX_EDU_DESCR_FR_LVL_1" AS tx_edu_descr_fr_lvl_1,
    "TX_EDU_DESCR_NL_LVL_1" AS tx_edu_descr_nl_lvl_1,
    "CD_AGE_LVL_0" AS cd_age_lvl_0,
    "CD_AGE_LVL_1" AS cd_age_lvl_1,
    "TX_AGE_DESCR_FR_LVL_1" AS tx_age_descr_fr_lvl_1,
    "TX_AGE_DESCR_NL_LVL_1" AS tx_age_descr_nl_lvl_1,
    "CD_AGE_LVL_2" AS cd_age_lvl_2,
    "TX_AGE_DESCR_FR_LVL_2" AS tx_age_descr_fr_lvl_2,
    "TX_AGE_DESCR_NL_LVL_2" AS tx_age_descr_nl_lvl_2,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "statbel-nodeid607"
