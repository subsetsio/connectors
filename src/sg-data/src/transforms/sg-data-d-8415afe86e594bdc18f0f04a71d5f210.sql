-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "road_type",
    "road_length"
FROM "sg-data-d-8415afe86e594bdc18f0f04a71d5f210"
