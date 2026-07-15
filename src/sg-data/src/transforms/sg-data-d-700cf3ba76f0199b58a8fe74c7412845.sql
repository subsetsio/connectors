-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "immunisation_type",
    "percent"
FROM "sg-data-d-700cf3ba76f0199b58a8fe74c7412845"
