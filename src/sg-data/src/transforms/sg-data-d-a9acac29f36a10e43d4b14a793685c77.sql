-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "policyholders",
    "policyholders_with_private_plans"
FROM "sg-data-d-a9acac29f36a10e43d4b14a793685c77"
