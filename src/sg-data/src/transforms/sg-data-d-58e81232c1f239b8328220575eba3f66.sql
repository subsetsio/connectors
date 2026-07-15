-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "admissions_by_age_group",
    "number_of_admissions"
FROM "sg-data-d-58e81232c1f239b8328220575eba3f66"
