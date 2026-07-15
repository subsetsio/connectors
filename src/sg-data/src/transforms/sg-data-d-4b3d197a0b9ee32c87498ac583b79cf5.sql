-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "cumulative_consumer_numbers",
    "cumulative_organisation_accounts",
    "cumulative_numbers_checked_million"
FROM "sg-data-d-4b3d197a0b9ee32c87498ac583b79cf5"
