-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "qt_lmdrs",
    "sector_of_school",
    "nw_lmdrs",
    "type_of_school",
    "no_of_schools"
FROM "qatar-planning-and-statistics-authority-number-of-schools-by-type-of-school-and-year"
