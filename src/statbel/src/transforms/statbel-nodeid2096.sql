-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_REFNIS" AS BIGINT) AS cd_refnis,
    "TX_DESCR_NL" AS tx_descr_nl,
    "TX_DESCR_FR" AS tx_descr_fr,
    CAST("CD_DSTR_REFNIS" AS BIGINT) AS cd_dstr_refnis,
    "TX_ADM_DSTR_DESCR_NL" AS tx_adm_dstr_descr_nl,
    "TX_ADM_DSTR_DESCR_FR" AS tx_adm_dstr_descr_fr,
    "CD_PROV_REFNIS" AS cd_prov_refnis,
    "TX_PROV_DESCR_NL" AS tx_prov_descr_nl,
    "TX_PROV_DESCR_FR" AS tx_prov_descr_fr,
    "CD_RGN_REFNIS" AS cd_rgn_refnis,
    "TX_RGN_DESCR_NL" AS tx_rgn_descr_nl,
    "TX_RGN_DESCR_FR" AS tx_rgn_descr_fr,
    "CD_SEX" AS cd_sex,
    "CD_NATLTY" AS cd_natlty,
    "TX_NATLTY_NL" AS tx_natlty_nl,
    "TX_NATLTY_FR" AS tx_natlty_fr,
    CAST("CD_CIV_STS" AS BIGINT) AS cd_civ_sts,
    "TX_CIV_STS_NL" AS tx_civ_sts_nl,
    "TX_CIV_STS_FR" AS tx_civ_sts_fr,
    CAST("CD_AGE" AS BIGINT) AS cd_age,
    CAST("MS_POPULATION" AS BIGINT) AS ms_population
FROM "statbel-nodeid2096"
