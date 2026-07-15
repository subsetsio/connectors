-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fare_type",
    "applicable_time",
    "distance",
    "fare_per_ride"
FROM "sg-data-d-2ca29f673b89e0cfddbb7c74516fa4d3"
