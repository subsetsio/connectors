-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "scientific_degree",
    "ldrj_l_lmy",
    "status",
    "lhl",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-new-students-and-graduates-abroad-by-scientific-degree-status-and-gender"
