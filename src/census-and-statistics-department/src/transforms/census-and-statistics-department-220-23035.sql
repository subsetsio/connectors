-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "IND" AS ind,
    CAST("CCYY" AS BIGINT) AS ccyy,
    "EMP_NATURE" AS emp_nature,
    "WWHGP" AS wwhgp,
    "obs_value",
    CAST("sd_value" AS BIGINT) AS sd_value,
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-220-23035"
