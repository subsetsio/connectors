-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "station",
    "total_installed_capacity_mig",
    "non_operating_capacity_mig",
    "operating_capacity_mig",
    "total_installed_capacity_m3",
    "non_operating_capacity_m3",
    "operating_capacity_m3"
FROM "qatar-planning-and-statistics-authority-water-storage-in-iwpp-reservoirs-2023"
