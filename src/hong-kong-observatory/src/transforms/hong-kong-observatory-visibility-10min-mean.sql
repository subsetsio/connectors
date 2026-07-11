-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a latest 10-minute mean visibility snapshot by station, not a historical time series.
SELECT
    CAST("observed_at" AS TIMESTAMP) AS observed_at,
    "station",
    "visibility"
FROM "hong-kong-observatory-visibility-10min-mean"
