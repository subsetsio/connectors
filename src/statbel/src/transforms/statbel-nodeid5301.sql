-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "DT_YR_STRT" AS dt_yr_strt,
    CAST("DT_YR" AS BIGINT) AS dt_yr,
    "CD_IND_NM_DE" AS cd_ind_nm_de,
    "CD_IND_NM_EN" AS cd_ind_nm_en,
    "CD_IND_NM_FR" AS cd_ind_nm_fr,
    "CD_IND_NM_NL" AS cd_ind_nm_nl,
    "CD_IND_VAL_DE" AS cd_ind_val_de,
    "CD_IND_VAL_EN" AS cd_ind_val_en,
    "CD_IND_VAL_FR" AS cd_ind_val_fr,
    "CD_IND_VAL_NL" AS cd_ind_val_nl,
    "CD_CAT_NM_DE" AS cd_cat_nm_de,
    "CD_CAT_NM_EN" AS cd_cat_nm_en,
    "CD_CAT_NM_FR" AS cd_cat_nm_fr,
    "CD_CAT_NM_NL" AS cd_cat_nm_nl,
    "CD_CAT_VAL_DE" AS cd_cat_val_de,
    "CD_CAT_VAL_EN" AS cd_cat_val_en,
    "CD_CAT_VAL_FR" AS cd_cat_val_fr,
    "CD_CAT_VAL_NL" AS cd_cat_val_nl,
    "MS_VAL" AS ms_val
FROM "statbel-nodeid5301"
