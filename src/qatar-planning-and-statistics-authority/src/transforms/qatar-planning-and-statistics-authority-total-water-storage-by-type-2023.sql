-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type",
    "lnw",
    "operating_reservoir_capacity_mig",
    "percentage",
    "remarks",
    "mlhzt"
FROM "qatar-planning-and-statistics-authority-total-water-storage-by-type-2023"
