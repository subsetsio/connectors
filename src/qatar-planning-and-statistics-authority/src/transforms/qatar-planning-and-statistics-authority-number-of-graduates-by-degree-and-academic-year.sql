-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "advance_diploma",
    "bachelor",
    "diploma",
    "master"
FROM "qatar-planning-and-statistics-authority-number-of-graduates-by-degree-and-academic-year"
