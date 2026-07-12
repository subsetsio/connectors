-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Observations span different economic measures and currencies; filter to comparable series before aggregating values.
SELECT
    "series_id",
    "group_id",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "value"
FROM "sveriges-riksbank-values"
