-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    "MONTH" AS month,
    "TX_LGL_CO_TYPE_FR_LVL1" AS tx_lgl_co_type_fr_lvl1,
    "TX_LGL_CO_TYPE_NL_LVL1" AS tx_lgl_co_type_nl_lvl1,
    "NACE1" AS nace1,
    "DESCR_NACE1_FR" AS descr_nace1_fr,
    "DESCR_NACE1_NL" AS descr_nace1_nl,
    "NACE2" AS nace2,
    "CD_REGION" AS cd_region,
    "TX_REGION_DESCR_NL" AS tx_region_descr_nl,
    "TX_REGION_DESCR_FR" AS tx_region_descr_fr,
    "MS_NUM_VAT_BOP" AS ms_num_vat_bop,
    "MS_NUM_VAT_FIRST_STRT" AS ms_num_vat_first_strt,
    "MS_NUM_VAT_RESTART" AS ms_num_vat_restart,
    "MS_NUM_VAT_STOP" AS ms_num_vat_stop,
    "MS_ADJUSMNT" AS ms_adjusmnt,
    "MS_NUM_REFNIS_IN" AS ms_num_refnis_in,
    "MS_NUM_REFNIS_OUT" AS ms_num_refnis_out,
    "MS_NUM_VAT_EOP" AS ms_num_vat_eop
FROM "statbel-nodeid3321"
