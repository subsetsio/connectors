-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("FFYY" AS BIGINT) AS ffyy,
    CAST("SUPPORT_TYPE" AS BIGINT) AS support_type,
    "obs_value",
    json_extract_string("sd_value", '$') AS sd_value,
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-710-86082"
