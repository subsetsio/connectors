-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "level_of_education",
    "lmstw_lt_lymy",
    "type_of_education",
    "nw_lt_lym",
    "gender",
    "ljns",
    "indicator",
    "lmw_shr",
    "number"
FROM "qatar-planning-and-statistics-authority-students-and-teachers-by-gender-type-of-education-and-level-of-education"
