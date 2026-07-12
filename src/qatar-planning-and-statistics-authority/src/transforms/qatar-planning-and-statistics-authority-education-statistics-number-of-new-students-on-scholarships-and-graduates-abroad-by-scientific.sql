-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "scientific_degree",
    "scientific_degree_ar",
    "gender",
    "gender_ar",
    "number_of_graduates_on_scholarships_abroad",
    "number_of_new_students_on_scholarships_abroad"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-new-students-on-scholarships-and-graduates-abroad-by-scientific"
