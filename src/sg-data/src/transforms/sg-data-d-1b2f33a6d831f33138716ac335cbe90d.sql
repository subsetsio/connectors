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
FROM "sg-data-d-1b2f33a6d831f33138716ac335cbe90d"
