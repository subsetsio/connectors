-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "housing_type",
    "computer_access_at_home"
FROM "sg-data-d-f078b7a2e3b220af4d3bfe676c4e7e69"
