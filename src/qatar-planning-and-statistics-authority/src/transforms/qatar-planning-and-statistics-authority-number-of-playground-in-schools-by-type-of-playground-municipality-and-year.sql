-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "qt_lmdrs",
    "sector_of_school",
    "lbldy",
    "municipality",
    "lnsht_lrydy",
    "type_of_playground",
    "no_of_playgrounds",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-number-of-playground-in-schools-by-type-of-playground-municipality-and-year"
