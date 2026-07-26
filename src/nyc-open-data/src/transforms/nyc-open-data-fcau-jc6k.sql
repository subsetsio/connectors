-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "materal_race_or_ethnicity",
    "infant_mortality_rate",
    "neonatal_mortality_rate",
    "postneonatal_mortality_rate",
    "infant_deaths",
    "neonatal_infant_deaths",
    "postneonatal_infant_deaths",
    "number_of_live_births"
FROM "nyc-open-data-fcau-jc6k"
