-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "production_mm3",
    "annual_growth",
    "average_growth_last_five_years"
FROM "qatar-planning-and-statistics-authority-total-annual-water-production-by-year"
