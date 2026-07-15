-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "status",
    "drug_of_abuse",
    "no_of_drug_abusers"
FROM "sg-data-d-63ddff57dda5ad302be6ae35a266af75"
