-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "crude_birth_rate_per_1_000_population",
    "crude_death_rate_per_1_000_population",
    "rate_of_natural_increase_per_1_000_population",
    "maternal_mortality_rate_per_100_000_live_births",
    "rate_of_deliveries_under_medical_supervision"
FROM "qatar-planning-and-statistics-authority-crude-birth-rate-crude-death-rates-and-rate-of-natural-increase"
