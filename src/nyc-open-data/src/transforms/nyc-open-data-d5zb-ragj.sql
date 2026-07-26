-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time_period",
    "page",
    "title",
    "visits",
    "_views" AS views,
    "average_time_viewed_seconds"
FROM "nyc-open-data-d5zb-ragj"
