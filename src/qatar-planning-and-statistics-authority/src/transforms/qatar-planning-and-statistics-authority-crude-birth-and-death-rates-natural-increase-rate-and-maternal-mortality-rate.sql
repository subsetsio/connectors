-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "rate_of_deliveries_under_medical_supervision",
    "maternal_mortality_rate_per_100000_live_birth",
    "natural_increase_per_1000_population",
    "crude_death_rate_per_1000_population",
    "crude_birth_rate_per_1000_population"
FROM "qatar-planning-and-statistics-authority-crude-birth-and-death-rates-natural-increase-rate-and-maternal-mortality-rate"
