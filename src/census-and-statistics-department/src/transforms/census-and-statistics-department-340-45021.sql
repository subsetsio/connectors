-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No scan-verifiable raw key: the 'DEP_P_T' dimension is NULL for stat_vars where that breakdown does not apply and '' for its own sub-total, so every column combination is unique but the key carries NULLs. Rows mix marginal totals (empty/NULL dimensions) with breakdowns — filter dimension columns before summing obs_value.
SELECT
    CAST("CCYY" AS BIGINT) AS ccyy,
    "MM" AS mm,
    "DEP_P_T" AS dep_p_t,
    "obs_value",
    CAST("sd_value" AS BIGINT) AS sd_value,
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-340-45021"
