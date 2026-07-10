-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("week_end", '%Y-%m-%d')::DATE AS week_end,
    "pathogen",
    CAST("percent_test_positivity" AS DOUBLE) AS percent_test_positivity
FROM "cdc-seuz-s2cv"
