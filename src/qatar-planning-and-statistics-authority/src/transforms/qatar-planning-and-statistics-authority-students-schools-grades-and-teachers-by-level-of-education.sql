-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "level_of_education",
    "lmstw_lt_lymy",
    "school_type",
    "nw_lmdrs",
    "indicator",
    "lmw_shr",
    "number"
FROM "qatar-planning-and-statistics-authority-students-schools-grades-and-teachers-by-level-of-education"
