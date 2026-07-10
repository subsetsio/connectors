-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("week_end", '%Y-%m-%d')::DATE AS week_end,
    "geography",
    "pathogen",
    "demographics_type",
    "demographics_values",
    CAST("percent_visits" AS DOUBLE) AS percent_visits
FROM "cdc-7xva-uux8"
