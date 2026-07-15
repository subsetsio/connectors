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
FROM "sg-data-d-7360b1a78d0bbde00461fa7d21326ec7"
