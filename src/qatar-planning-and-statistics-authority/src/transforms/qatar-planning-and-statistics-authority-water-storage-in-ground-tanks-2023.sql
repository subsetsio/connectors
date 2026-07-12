-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "location",
    "lmwq",
    "ground_tank_non_operating_mig",
    "ground_tank_operating_mig",
    "ground_tank_non_operating_m3",
    "ground_tank_operating_m3",
    "remarks",
    "mlhzt"
FROM "qatar-planning-and-statistics-authority-water-storage-in-ground-tanks-2023"
