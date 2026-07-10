-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    CAST("CD_LGL_CO_TYP" AS BIGINT) AS cd_lgl_co_typ,
    "TX_LGL_CO_TYP_FR" AS tx_lgl_co_typ_fr,
    "TX_LGL_CO_TYP_NL" AS tx_lgl_co_typ_nl,
    "TX_LGL_CO_TYP_EN" AS tx_lgl_co_typ_en,
    "CD_RGN_REFNIS" AS cd_rgn_refnis,
    "TX_RGN_DESCR_FR" AS tx_rgn_descr_fr,
    "TX_RGN_DESCR_NL" AS tx_rgn_descr_nl,
    "TX_RGN_DESCR_EN" AS tx_rgn_descr_en,
    "CD_PROV_REFNIS" AS cd_prov_refnis,
    "TX_PROV_DESCR_FR" AS tx_prov_descr_fr,
    "TX_PROV_DESCR_NL" AS tx_prov_descr_nl,
    "TX_PROV_DESCR_EN" AS tx_prov_descr_en,
    "CD_CLS_WRKR" AS cd_cls_wrkr,
    "TX_CLS_WRKR_FR" AS tx_cls_wrkr_fr,
    "TX_CLS_WRKR_NL" AS tx_cls_wrkr_nl,
    "TX_CLS_WRKR_EN" AS tx_cls_wrkr_en,
    "CD_NACE_LVL1" AS cd_nace_lvl1,
    "TX_NACE_LVL1_DESCR_FR" AS tx_nace_lvl1_descr_fr,
    "TX_NACE_LVL1_DESCR_NL" AS tx_nace_lvl1_descr_nl,
    "TX_NACE_LVL1_DESCR_EN" AS tx_nace_lvl1_descr_en,
    "CD_NACE_LVL2" AS cd_nace_lvl2,
    "TX_NACE_LVL2_DESCR_FR" AS tx_nace_lvl2_descr_fr,
    "TX_NACE_LVL2_DESCR_NL" AS tx_nace_lvl2_descr_nl,
    "TX_NACE_LVL2_DESCR_EN" AS tx_nace_lvl2_descr_en,
    CAST("MS_CNT_FIRST_REGISTRATIONS" AS BIGINT) AS ms_cnt_first_registrations,
    CAST("MS_CNT_SURV_YEAR_1" AS BIGINT) AS ms_cnt_surv_year_1,
    "MS_CNT_SURV_YEAR_2" AS ms_cnt_surv_year_2,
    "MS_CNT_SURV_YEAR_3" AS ms_cnt_surv_year_3,
    "MS_CNT_SURV_YEAR_4" AS ms_cnt_surv_year_4,
    "MS_CNT_SURV_YEAR_5" AS ms_cnt_surv_year_5
FROM "statbel-nodeid6279"
