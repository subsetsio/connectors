-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "admissions_by_age_group",
    "number_of_admissions"
FROM "sg-data-d-30868b21a990a0bd15f8e5e2ff1ce489"
