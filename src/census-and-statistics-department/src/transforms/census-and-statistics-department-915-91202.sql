-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Q" AS q,
    CAST("CCYY" AS BIGINT) AS ccyy,
    "USER_TYPE" AS user_type,
    "obs_value",
    json_extract_string("sd_value", '$') AS sd_value,
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-915-91202"
