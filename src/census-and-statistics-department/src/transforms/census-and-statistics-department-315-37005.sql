-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "BOP_COMPONENT" AS bop_component,
    CAST("CCYY" AS BIGINT) AS ccyy,
    CAST("Q" AS BIGINT) AS q,
    "obs_value",
    "sd_value",
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-315-37005"
