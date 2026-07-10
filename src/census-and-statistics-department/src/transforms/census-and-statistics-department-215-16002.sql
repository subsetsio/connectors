-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No scan-verifiable raw key: the 'SEX' dimension is NULL for stat_vars where that breakdown does not apply and '' for its own sub-total, so every column combination is unique but the key carries NULLs. Rows mix marginal totals (empty/NULL dimensions) with breakdowns — filter dimension columns before summing obs_value.
SELECT
    "DC" AS dc,
    "IND" AS ind,
    CAST("CCYY" AS BIGINT) AS ccyy,
    CAST("MM" AS BIGINT) AS mm,
    "obs_value",
    json_extract_string("sd_value", '$') AS sd_value,
    "stat_var",
    "stat_pres",
    json_extract_string("SEX", '$') AS sex
FROM "census-and-statistics-department-215-16002"
