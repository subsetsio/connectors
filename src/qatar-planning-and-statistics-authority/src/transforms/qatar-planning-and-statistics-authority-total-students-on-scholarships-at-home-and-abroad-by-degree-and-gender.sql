-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "type_of_scholarship",
    "scientific_degree",
    "gender",
    "number_of_students_dd_ltlb",
    "lnw",
    "ldrj_l_lmy",
    "nw_lmnh"
FROM "qatar-planning-and-statistics-authority-total-students-on-scholarships-at-home-and-abroad-by-degree-and-gender"
