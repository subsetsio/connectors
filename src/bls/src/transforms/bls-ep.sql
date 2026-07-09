-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `rank_code` and `disp_code` (employment level vs rank vs change). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `occ_code` and `ind_code` are SOC/NAICS hierarchies carrying 'Total, all occupations' and 'Total, all industries' rows alongside their components; `occ_type`/`ind_type` flag which level a row sits at.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "seasonal",
    "seasonal_name",
    "occ_type",
    "ind_type",
    "occ_code",
    "ind_code",
    CAST("wkex_code" AS BIGINT) AS wkex_code,
    "wkex_name",
    CAST("rank_code" AS BIGINT) AS rank_code,
    CAST("otjt_code" AS BIGINT) AS otjt_code,
    "otjt_name",
    CAST("eductrn_code" AS BIGINT) AS eductrn_code,
    CAST("disp_code" AS BIGINT) AS disp_code,
    "series_title"
FROM "bls-ep"
