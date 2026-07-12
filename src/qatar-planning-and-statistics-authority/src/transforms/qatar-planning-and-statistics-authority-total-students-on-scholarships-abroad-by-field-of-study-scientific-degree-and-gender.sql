-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "field_of_study",
    "scientific_degree",
    "gender",
    "number_of_students_dd_ltlb",
    "lnw",
    "ldrj_l_lmy",
    "mjl_ldrs"
FROM "qatar-planning-and-statistics-authority-total-students-on-scholarships-abroad-by-field-of-study-scientific-degree-and-gender"
