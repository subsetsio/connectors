-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "date",
    CAST("statefips" AS BIGINT) AS statefips,
    CAST("countyfips" AS BIGINT) AS countyfips,
    CAST("o3_max_pred" AS DOUBLE) AS o3_max_pred,
    CAST("o3_med_pred" AS DOUBLE) AS o3_med_pred,
    CAST("o3_mean_pred" AS DOUBLE) AS o3_mean_pred,
    CAST("o3_pop_pred" AS DOUBLE) AS o3_pop_pred
FROM "cdc-3vxk-q2jk"
