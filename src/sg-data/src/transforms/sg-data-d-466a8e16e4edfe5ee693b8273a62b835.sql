-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "AgeGroup" AS agegroup,
    "Sex" AS sex,
    "Barriers" AS barriers,
    "Percentage" AS percentage
FROM "sg-data-d-466a8e16e4edfe5ee693b8273a62b835"
