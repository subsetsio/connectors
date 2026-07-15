-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no_of_lic_nt_renewed"
FROM "sg-data-d-59a1bad53ad1bce570aa4c7ed169ebf1"
