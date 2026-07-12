-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no_of_water_tankers",
    "no_of_km_rented_water_tankers",
    "total_reduction",
    "total_reduction0",
    "km_rented_reduction",
    "km_rented_reduction0"
FROM "qatar-planning-and-statistics-authority-water-tanker-services-by-year"
