-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "consumer_numbers",
    "organisation_accounts",
    "numbers_checked_million"
FROM "sg-data-d-01f9a96040aff275cf4747712c7fcdda"
