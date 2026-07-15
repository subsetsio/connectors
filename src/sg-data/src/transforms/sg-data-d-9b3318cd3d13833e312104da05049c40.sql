-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "status",
    "age_group",
    "no_of_drug_abusers"
FROM "sg-data-d-9b3318cd3d13833e312104da05049c40"
