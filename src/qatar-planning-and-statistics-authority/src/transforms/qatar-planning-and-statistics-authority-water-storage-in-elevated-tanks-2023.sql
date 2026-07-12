-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "location",
    "lmwq",
    "elevated_tank_capacity_imperial_gallons",
    "elevated_tank_operating_capacity_imperial_gallons",
    "capacity_m3",
    "operating_capacity_m3",
    "remarks",
    "mlhzt"
FROM "qatar-planning-and-statistics-authority-water-storage-in-elevated-tanks-2023"
