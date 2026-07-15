-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "constituency",
    "constituency_type",
    "candidates",
    "party",
    "vote_count",
    "vote_percentage"
FROM "sg-data-d-ba8da764a37ca36b34e4e5ad866294f8"
