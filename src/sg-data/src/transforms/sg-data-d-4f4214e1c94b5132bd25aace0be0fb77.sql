-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Citizenship" AS citizenship,
    "Semester" AS semester,
    "Fees" AS fees,
    "Reference" AS reference
FROM "sg-data-d-4f4214e1c94b5132bd25aace0be0fb77"
