-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("NM_YR" AS BIGINT) AS nm_yr,
    CAST("NM_MTH" AS BIGINT) AS nm_mth,
    CAST("MS_CPI_IDX" AS DOUBLE) AS ms_cpi_idx,
    "MS_CPI_INFL" AS ms_cpi_infl,
    CAST("MS_WT_CPI" AS BIGINT) AS ms_wt_cpi,
    "MS_HLTH_IDX" AS ms_hlth_idx,
    "FREQ" AS freq,
    CAST("NM_BASE_YR" AS BIGINT) AS nm_base_yr,
    "MS_WTHOUT_ENE_IDX" AS ms_wthout_ene_idx,
    "MS_WITHOUT_PTRL_IDX" AS ms_without_ptrl_idx,
    "MS_SMOOTH_IDX" AS ms_smooth_idx
FROM "statbel-nodeid669"
