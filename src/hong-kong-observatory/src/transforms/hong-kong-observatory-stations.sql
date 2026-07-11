-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The same station code may appear in more than one dataset group when it is used by multiple Hong Kong Observatory products.
SELECT
    "station_code",
    "dataset_group"
FROM "hong-kong-observatory-stations"
