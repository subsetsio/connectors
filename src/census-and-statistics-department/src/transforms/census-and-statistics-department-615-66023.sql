-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("BTG_GRP" AS BIGINT) AS btg_grp,
    "USE_GRP" AS use_grp,
    CAST("CCYY" AS BIGINT) AS ccyy,
    "Q" AS q,
    "obs_value",
    CAST("sd_value" AS BIGINT) AS sd_value,
    "stat_var",
    "stat_pres"
FROM "census-and-statistics-department-615-66023"
