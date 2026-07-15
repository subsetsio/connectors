-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mode",
    "ave_distance_per_trip"
FROM "sg-data-d-1e8c9a3f599bca92c76bdb7d8a52a79a"
