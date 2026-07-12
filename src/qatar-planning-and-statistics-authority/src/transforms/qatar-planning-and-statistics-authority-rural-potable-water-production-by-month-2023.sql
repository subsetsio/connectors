-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "judiyah_well_field",
    "rushaidah_well_field",
    "total_abu_samra_north_camp_r_o_plant_production"
FROM "qatar-planning-and-statistics-authority-rural-potable-water-production-by-month-2023"
