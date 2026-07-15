-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "page",
    "Impressions" AS impressions,
    "Clicks" AS clicks,
    "Click_through_rate" AS click_through_rate,
    "Position" AS position
FROM "sg-data-d-78853d8f18e64df6836077d33d44375a"
