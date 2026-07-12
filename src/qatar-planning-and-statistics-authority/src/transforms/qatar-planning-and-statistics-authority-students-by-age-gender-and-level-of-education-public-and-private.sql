-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "age",
    "educational_stage",
    "lmrhl_lt_lymy",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-students-by-age-gender-and-level-of-education-public-and-private"
