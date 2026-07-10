-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "CD_RGN_REFNIS_RESIDENCE" AS cd_rgn_refnis_residence,
    "TX_RGN_RESIDENCE_DESCR_NL" AS tx_rgn_residence_descr_nl,
    "TX_RGN_RESIDENCE_DESCR_FR" AS tx_rgn_residence_descr_fr,
    "CD_PROV_REFNIS_RESIDENCE" AS cd_prov_refnis_residence,
    "TX_PROV_RESIDENCE_DESCR_NL" AS tx_prov_residence_descr_nl,
    "TX_PROV_RESIDENCE_DESCR_FR" AS tx_prov_residence_descr_fr,
    CAST("CD_DSTR_REFNIS_RESIDENCE" AS BIGINT) AS cd_dstr_refnis_residence,
    "TX_ADM_DSTR_RESIDENCE_DESCR_NL" AS tx_adm_dstr_residence_descr_nl,
    "TX_ADM_DSTR_RESIDENCE_DESCR_FR" AS tx_adm_dstr_residence_descr_fr,
    CAST("CD_MUNTY_REFNIS_RESIDENCE" AS BIGINT) AS cd_munty_refnis_residence,
    "TX_MUNTY_RESIDENCE_DESCR_NL" AS tx_munty_residence_descr_nl,
    "TX_MUNTY_RESIDENCE_DESCR_FR" AS tx_munty_residence_descr_fr,
    CAST("XY_X_LB_72_RESIDENCE" AS BIGINT) AS xy_x_lb_72_residence,
    CAST("XY_Y_LB_72_RESIDENCE" AS BIGINT) AS xy_y_lb_72_residence,
    "CD_CNTRY_REFNIS_WORK" AS cd_cntry_refnis_work,
    "TX_CNTRY_WORK_DESCR_NL" AS tx_cntry_work_descr_nl,
    "TX_CNTRY_WORK_DESCR_FR" AS tx_cntry_work_descr_fr,
    "CD_RGN_REFNIS_WORK" AS cd_rgn_refnis_work,
    "TX_RGN_WORK_DESCR_NL" AS tx_rgn_work_descr_nl,
    "TX_RGN_WORK_DESCR_FR" AS tx_rgn_work_descr_fr,
    "CD_PROV_REFNIS_WORK" AS cd_prov_refnis_work,
    "TX_PROV_WORK_DESCR_NL" AS tx_prov_work_descr_nl,
    "TX_PROV_WORK_DESCR_FR" AS tx_prov_work_descr_fr,
    "CD_DSTR_REFNIS_WORK" AS cd_dstr_refnis_work,
    "TX_ADM_DSTR_WORK_DESCR_NL" AS tx_adm_dstr_work_descr_nl,
    "TX_ADM_DSTR_WORK_DESCR_FR" AS tx_adm_dstr_work_descr_fr,
    "CD_MUNTY_REFNIS_WORK" AS cd_munty_refnis_work,
    "TX_MUNTY_WORK_DESCR_NL" AS tx_munty_work_descr_nl,
    "TX_MUNTY_WORK_DESCR_FR" AS tx_munty_work_descr_fr,
    "XY_X_LB_72_WORK" AS xy_x_lb_72_work,
    "XY_Y_LB_72_WORK" AS xy_y_lb_72_work,
    "CD_SEX" AS cd_sex,
    "TX_SEX_DESCR_NL" AS tx_sex_descr_nl,
    "TX_SEX_DESCR_FR" AS tx_sex_descr_fr,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "statbel-nodeid594"
