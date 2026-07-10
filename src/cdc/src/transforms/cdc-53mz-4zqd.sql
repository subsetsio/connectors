-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "date",
    CAST("statefips" AS BIGINT) AS statefips,
    CAST("countyfips" AS BIGINT) AS countyfips,
    CAST("pm25_max_pred" AS DOUBLE) AS pm25_max_pred,
    CAST("pm25_med_pred" AS DOUBLE) AS pm25_med_pred,
    CAST("pm25_mean_pred" AS DOUBLE) AS pm25_mean_pred,
    CAST("pm25_pop_pred" AS DOUBLE) AS pm25_pop_pred
FROM "cdc-53mz-4zqd"
