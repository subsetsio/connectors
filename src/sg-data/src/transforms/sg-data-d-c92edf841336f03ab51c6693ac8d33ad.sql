-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "temp_mean_daily_min"
FROM "sg-data-d-c92edf841336f03ab51c6693ac8d33ad"
