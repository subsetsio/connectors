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
FROM "sg-data-d-973a5c8e191baa29bf4e3826500d13b3"
