-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DC" AS dc,
    CAST("CCYY" AS BIGINT) AS ccyy,
    "TENURE" AS tenure,
    "obs_value",
    json_extract_string("sd_value", '$') AS sd_value,
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-130-06803"
