-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "abstraction_from_ground_water_by_types_mm3",
    "agricultural_wells",
    "municipal_wells_domestic_wells_and_industrial_wells",
    "other_wells"
FROM "qatar-planning-and-statistics-authority-total-water-storage-2023"
