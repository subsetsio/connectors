-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_interest_groups",
    "no_of_members"
FROM "sg-data-d-7a5534d2877ad45b5369ccefc49739a7"
