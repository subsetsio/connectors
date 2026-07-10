-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    CAST("CD_MUNTY_REFNIS" AS BIGINT) AS cd_munty_refnis,
    CAST("MS_NBR_ELIGIBLE" AS BIGINT) AS ms_nbr_eligible,
    CAST("MS_NBR_NOT_ELIGIBLE" AS BIGINT) AS ms_nbr_not_eligible,
    CAST("MS_PERC_NOT_ELIGIBLE" AS DOUBLE) AS ms_perc_not_eligible,
    CAST("MS_PERC_IOE_HH" AS DOUBLE) AS ms_perc_ioe_hh,
    "MS_Q1" AS ms_q1,
    "MS_MEDIAN" AS ms_median,
    "MS_Q3" AS ms_q3,
    "MS_INT_QUART_DIFF" AS ms_int_quart_diff,
    "MS_ADMIN_AROP" AS ms_admin_arop,
    "TX_MUNTY_DESCR_NL" AS tx_munty_descr_nl,
    "TX_MUNTY_DESCR_FR" AS tx_munty_descr_fr,
    "TX_MUNTY_DESCR_EN" AS tx_munty_descr_en,
    "TX_MUNTY_DESCR_DE" AS tx_munty_descr_de,
    CAST("CD_DSTR_REFNIS" AS BIGINT) AS cd_dstr_refnis,
    "TX_DSTR_DESCR_NL" AS tx_dstr_descr_nl,
    "TX_DSTR_DESCR_FR" AS tx_dstr_descr_fr,
    "TX_DSTR_DESCR_EN" AS tx_dstr_descr_en,
    "TX_DSTR_DESCR_DE" AS tx_dstr_descr_de,
    CAST("CD_PROV_REFNIS" AS BIGINT) AS cd_prov_refnis,
    "TX_PROV_DESCR_NL" AS tx_prov_descr_nl,
    "TX_PROV_DESCR_FR" AS tx_prov_descr_fr,
    "TX_PROV_DESCR_EN" AS tx_prov_descr_en,
    "TX_PROV_DESCR_DE" AS tx_prov_descr_de,
    "CD_RGN_REFNIS" AS cd_rgn_refnis,
    "TX_RGN_DESCR_NL" AS tx_rgn_descr_nl,
    "TX_RGN_DESCR_FR" AS tx_rgn_descr_fr,
    "TX_RGN_DESCR_EN" AS tx_rgn_descr_en,
    "TX_RGN_DESCR_DE" AS tx_rgn_descr_de
FROM "statbel-nodeid5465"
