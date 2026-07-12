-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "census_year",
    "municipality",
    "municipality_arabic",
    "municipality_area_km_2",
    "population",
    "population_density",
    "population0"
FROM "qatar-planning-and-statistics-authority-total-population-and-population-density-by-municipality-in-census-2010-2020"
