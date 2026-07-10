-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No scan-verifiable raw key: the 'GDP_COMPONENT' dimension is NULL for stat_vars where that breakdown does not apply and '' for its own sub-total, so every column combination is unique but the key carries NULLs. Rows mix marginal totals (empty/NULL dimensions) with breakdowns — filter dimension columns before summing obs_value.
SELECT
    "GDP_COMPONENT" AS gdp_component,
    CAST("CCYY" AS BIGINT) AS ccyy,
    "Q" AS q,
    "obs_value",
    "sd_value",
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-310-30001"
