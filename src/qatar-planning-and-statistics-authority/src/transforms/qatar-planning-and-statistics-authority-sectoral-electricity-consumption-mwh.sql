-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "bulk_industrial",
    "domestic",
    "auxiliary",
    "transmission_and_distribution_losses",
    "total_injected_generation",
    "total_electricity_generation"
FROM "qatar-planning-and-statistics-authority-sectoral-electricity-consumption-mwh"
