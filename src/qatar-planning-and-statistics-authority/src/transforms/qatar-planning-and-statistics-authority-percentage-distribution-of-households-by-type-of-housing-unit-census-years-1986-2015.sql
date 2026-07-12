-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_housing_unit",
    "nw_lwhd_lskny",
    "1986",
    "1997",
    "2004",
    "2010",
    "2015",
    "growth_rate_2010_2015"
FROM "qatar-planning-and-statistics-authority-percentage-distribution-of-households-by-type-of-housing-unit-census-years-1986-2015"
