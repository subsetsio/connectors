-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "M3M" AS m3m,
    "MIND" AS mind,
    CAST("CCYY" AS BIGINT) AS ccyy,
    "obs_value",
    "sd_value",
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-210-06503"
