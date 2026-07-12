-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "indicator_name",
    "water_potentially_available_for_use",
    "water_use_and_losses",
    "remarks"
FROM "qatar-planning-and-statistics-authority-details-of-water-use-balance-water-balance-million-m3"
