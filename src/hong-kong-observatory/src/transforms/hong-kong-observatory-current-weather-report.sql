-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the latest report snapshot, not an accumulated history; each run overwrites the current conditions available at collection time.
SELECT
    CAST("update_time" AS TIMESTAMP) AS update_time,
    "category",
    "place",
    "value",
    "unit"
FROM "hong-kong-observatory-current-weather-report"
