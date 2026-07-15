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
FROM "sg-data-d-581a30bee57fa7d8383d6bc94739ad00"
