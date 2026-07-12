-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "field_of_study",
    "mjl_ldrs",
    "scientific_degree",
    "ldrj_l_lmy",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-total-students-on-scholarships-abroad-by-specialization-and-scientific-degree"
