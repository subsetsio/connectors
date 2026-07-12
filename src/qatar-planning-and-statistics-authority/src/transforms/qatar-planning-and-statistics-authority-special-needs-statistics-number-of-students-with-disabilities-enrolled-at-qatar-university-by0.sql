-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "gender",
    "number_of_students",
    "gender_ar",
    "nationality_ar"
FROM "qatar-planning-and-statistics-authority-special-needs-statistics-number-of-students-with-disabilities-enrolled-at-qatar-university-by0"
