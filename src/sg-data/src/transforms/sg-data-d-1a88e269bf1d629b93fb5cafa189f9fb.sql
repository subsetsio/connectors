-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age",
    "media_activity",
    "sample_size",
    "ever_used"
FROM "sg-data-d-1a88e269bf1d629b93fb5cafa189f9fb"
