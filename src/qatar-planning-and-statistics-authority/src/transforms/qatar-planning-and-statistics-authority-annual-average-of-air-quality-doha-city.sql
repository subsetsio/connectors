-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "location",
    "sulfur_dioxide_so2",
    "nitrogen_dioxide_no2",
    "ground_level_ozone_o3",
    "carbon_monoxide_co",
    "particulate_matter_pm10"
FROM "qatar-planning-and-statistics-authority-annual-average-of-air-quality-doha-city"
