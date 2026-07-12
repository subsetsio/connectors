-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "level_of_education",
    "lmstw_lt_lymy",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-persons-attending-night-schools-and-illiteracy-eradication-centers-by-level-of-education-and-gender"
