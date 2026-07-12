-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "level_of_education_ar",
    "grade",
    "grade_ar",
    "nationality",
    "nationality_ar",
    "gender",
    "gender_ar",
    "number_of_persons_dd_l_shkhs"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-persons-attending-evening-schools-and-illiteracy-eradication-centers"
