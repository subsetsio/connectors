-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "imperial_gallons_ig",
    "meter_cube_m3",
    "million_meter_cube_mm3",
    "million_imperial_gallons_mig"
FROM "qatar-planning-and-statistics-authority-total-water-storage-by-year"
