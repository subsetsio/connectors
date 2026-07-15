-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "temp_mean_daily_min"
FROM "sg-data-d-be96fc5a86b96f228efd7addaf7e61a8"
