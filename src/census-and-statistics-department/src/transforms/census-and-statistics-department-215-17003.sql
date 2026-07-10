-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("CCYY" AS BIGINT) AS ccyy,
    CAST("MM" AS BIGINT) AS mm,
    "END_USE" AS end_use,
    "SECTOR" AS sector,
    "obs_value",
    CAST("sd_value" AS BIGINT) AS sd_value,
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-215-17003"
