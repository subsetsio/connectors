-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_LGL_PSN_VAT" AS BIGINT) AS cd_lgl_psn_vat,
    "TX_LGL_PSN_VAT_FR_LVL1" AS tx_lgl_psn_vat_fr_lvl1,
    "TX_LGL_PSN_VAT_NL_LVL1" AS tx_lgl_psn_vat_nl_lvl1,
    "TX_LGL_PSN_VAT_EN_LVL1" AS tx_lgl_psn_vat_en_lvl1,
    "CD_NACE" AS cd_nace,
    "TX_NACE_FR_LVL1" AS tx_nace_fr_lvl1,
    "TX_NACE_NL_LVL1" AS tx_nace_nl_lvl1,
    "TX_NACE_EN_LVL1" AS tx_nace_en_lvl1,
    "TX_NACE_FR_LVL2" AS tx_nace_fr_lvl2,
    "TX_NACE_NL_LVL2" AS tx_nace_nl_lvl2,
    "TX_NACE_EN_LVL2" AS tx_nace_en_lvl2,
    "TX_NACE_FR_LVL3" AS tx_nace_fr_lvl3,
    "TX_NACE_NL_LVL3" AS tx_nace_nl_lvl3,
    "TX_NACE_EN_LVL3" AS tx_nace_en_lvl3,
    "TX_NACE_FR_LVL4" AS tx_nace_fr_lvl4,
    "TX_NACE_NL_LVL4" AS tx_nace_nl_lvl4,
    "TX_NACE_EN_LVL4" AS tx_nace_en_lvl4,
    "TX_NACE_FR_LVL5" AS tx_nace_fr_lvl5,
    "TX_NACE_NL_LVL5" AS tx_nace_nl_lvl5,
    "TX_NACE_EN_LVL5" AS tx_nace_en_lvl5,
    "CD_MUNTY_REFNIS" AS cd_munty_refnis,
    "TX_MUNTY_DESCR_FR" AS tx_munty_descr_fr,
    "TX_MUNTY_DESCR_NL" AS tx_munty_descr_nl,
    "TX_MUNTY_DESCR_EN" AS tx_munty_descr_en,
    "CD_ADM_DSTR_REFNIS" AS cd_adm_dstr_refnis,
    "TX_ADM_DSTR_DESCR_FR" AS tx_adm_dstr_descr_fr,
    "TX_ADM_DSTR_DESCR_NL" AS tx_adm_dstr_descr_nl,
    "TX_ADM_DSTR_DESCR_EN" AS tx_adm_dstr_descr_en,
    "CD_RGN_REFNIS" AS cd_rgn_refnis,
    "CD_PROV_REFNIS" AS cd_prov_refnis,
    "TX_PROV_DESCR_FR" AS tx_prov_descr_fr,
    "TX_PROV_DESCR_NL" AS tx_prov_descr_nl,
    "TX_PROV_DESCR_EN" AS tx_prov_descr_en,
    "TX_RGN_DESCR_FR" AS tx_rgn_descr_fr,
    "TX_RGN_DESCR_NL" AS tx_rgn_descr_nl,
    "TX_RGN_DESCR_EN" AS tx_rgn_descr_en,
    CAST("MS_NUM_VAT" AS BIGINT) AS ms_num_vat,
    CAST("MS_NUM_VAT_START" AS BIGINT) AS ms_num_vat_start,
    CAST("MS_NUM_VAT_STOP" AS BIGINT) AS ms_num_vat_stop
FROM "statbel-nodeid6466"
