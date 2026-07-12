-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "iwpps",
    "water_production_million_cubic_meters",
    "million_imperial_gallons_mig"
FROM "qatar-planning-and-statistics-authority-water-production-by-independent-water-and-power-producers-iwpps"
