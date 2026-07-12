-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "field_of_study",
    "field_of_study_ar",
    "number_of_graduates_males",
    "number_of_graduates_females"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-graduates-on-scholarships-abroad-by-field-of-study-and-gender"
