-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "number_of_zone",
    "lmntq",
    "zone",
    "population",
    "area_in_km",
    "population_density_km2"
FROM "qatar-planning-and-statistics-authority-population-area-and-population-density-per-square-kilometers-by-zone"
