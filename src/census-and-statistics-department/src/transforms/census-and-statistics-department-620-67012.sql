-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("CCYY" AS BIGINT) AS ccyy,
    "MM" AS mm,
    "BROAD_PROD_CAT" AS broad_prod_cat,
    CAST("OUTLET_TYPE" AS BIGINT) AS outlet_type,
    "obs_value",
    CAST("sd_value" AS BIGINT) AS sd_value,
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-620-67012"
