-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name_of_charity",
    "sector_or_beneficiaries"
FROM "sg-data-d-7249aa8080c2e3211fd1c5811e507bff"
