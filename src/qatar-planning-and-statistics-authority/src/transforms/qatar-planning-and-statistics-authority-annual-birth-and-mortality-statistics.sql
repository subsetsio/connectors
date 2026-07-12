-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "number_of_live_births",
    "number_of_deaths",
    "neonatal_mortality_rate_per_1_000_live_births",
    "infant_mortality_rate_per_1_000_live_births",
    "under_5_mortality_rate_per_1_000_live_births",
    "maternal_mortality_ratio_per_100_000_live_births"
FROM "qatar-planning-and-statistics-authority-annual-birth-and-mortality-statistics"
