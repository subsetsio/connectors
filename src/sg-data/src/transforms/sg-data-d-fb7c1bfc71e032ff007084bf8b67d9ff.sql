-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "Queries" AS queries,
    "Clicks" AS clicks,
    "Impressions" AS impressions,
    "Click_through_rate" AS click_through_rate,
    "Position" AS position
FROM "sg-data-d-fb7c1bfc71e032ff007084bf8b67d9ff"
