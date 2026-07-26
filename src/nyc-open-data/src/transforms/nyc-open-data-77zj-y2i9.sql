-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pub_dt",
    "agy_cd",
    "agy_nm",
    "curr_yr",
    "dbt_lmt_cls",
    "cat_nm",
    "subcat_nm",
    "curr_yr_outstd_amt",
    "nxt_yr_int",
    "nxt_yr_redpt_amt"
FROM "nyc-open-data-77zj-y2i9"
