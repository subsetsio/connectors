-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "week_end",
    "condition",
    CAST("percent_visits" AS DOUBLE) AS percent_visits,
    "age_group"
FROM "cdc-v58w-vynu"
