-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "potable_water_used_mm3_year",
    "non_potable_water_used_mm3_year",
    "total_makeup_water_demand_mm3_year"
FROM "qatar-planning-and-statistics-authority-non-potable-water-used-in-district-cooling"
