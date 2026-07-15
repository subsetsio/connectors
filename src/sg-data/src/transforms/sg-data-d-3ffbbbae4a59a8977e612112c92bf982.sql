-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "admissions_by_education_level",
    "number_of_admissions"
FROM "sg-data-d-3ffbbbae4a59a8977e612112c92bf982"
