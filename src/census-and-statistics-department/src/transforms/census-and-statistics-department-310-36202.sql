-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("CCYY" AS BIGINT) AS ccyy,
    "Q" AS q,
    "FLOWS" AS flows,
    "INC_CPNT" AS inc_cpnt,
    "obs_value",
    "sd_value",
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-310-36202"
