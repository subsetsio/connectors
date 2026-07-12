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
    "nw_sh_ll_b",
    "type_of_playground",
    "no_of_playgrounds"
FROM "qatar-planning-and-statistics-authority-playground-in-schools-by-education-level-type-of-playground-and-year"
