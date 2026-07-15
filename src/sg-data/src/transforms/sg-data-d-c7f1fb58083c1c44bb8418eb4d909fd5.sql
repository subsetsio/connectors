-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "candidates",
    "vote_count",
    "vote_percentage"
FROM "sg-data-d-c7f1fb58083c1c44bb8418eb4d909fd5"
