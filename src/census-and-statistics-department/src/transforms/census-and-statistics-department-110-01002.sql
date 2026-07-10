-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SEX" AS sex,
    "AGE" AS age,
    CAST("H" AS BIGINT) AS h,
    CAST("CCYY" AS BIGINT) AS ccyy,
    "obs_value",
    CAST("sd_value" AS BIGINT) AS sd_value,
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-110-01002"
