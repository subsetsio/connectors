-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "water_production_mm3",
    "change_production",
    "max_daily_production_mm3_day",
    "change_max_prod",
    "no_of_customers_incl_tankers",
    "change_customers"
FROM "qatar-planning-and-statistics-authority-key-water-growth-indicators"
