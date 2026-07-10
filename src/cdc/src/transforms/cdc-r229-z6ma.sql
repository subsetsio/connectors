-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("mmwr_week_end", '%m/%d/%Y')::DATE AS mmwr_week_end,
    "pathogen",
    CAST("n_enrolled" AS BIGINT) AS n_enrolled,
    CAST("pct_positive" AS DOUBLE) AS pct_positive,
    CAST("mmwr_week" AS BIGINT) AS mmwr_week,
    "footnote"
FROM "cdc-r229-z6ma"
