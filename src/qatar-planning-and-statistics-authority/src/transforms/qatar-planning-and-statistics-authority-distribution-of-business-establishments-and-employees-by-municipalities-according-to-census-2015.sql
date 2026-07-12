-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "lbldy",
    "establishments_number_dd_lmnshat",
    "establishments_lmnshat",
    "employees_number_dd_lmshtglwn",
    "employees_lmshtglwn",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-distribution-of-business-establishments-and-employees-by-municipalities-according-to-census-2015"
