-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cohort",
    "enrolled_students",
    "graduates",
    "annual_graduation_rate"
FROM "qatar-planning-and-statistics-authority-annual-graduation-rate-by-student-cohort"
