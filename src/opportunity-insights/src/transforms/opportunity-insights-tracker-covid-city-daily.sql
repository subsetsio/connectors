-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "day",
    "cityid",
    "case_count",
    "death_count",
    "new_case_count",
    "new_death_count",
    "vaccine_count",
    "new_vaccine_count",
    "fullvaccine_count",
    "new_fullvaccine_count",
    "booster_first_count",
    "new_booster_first_count",
    "test_count",
    "new_test_count",
    "new_case_rate",
    "case_rate",
    "new_death_rate",
    "death_rate",
    "new_test_rate",
    "test_rate",
    "new_vaccine_rate",
    "vaccine_rate",
    "new_fullvaccine_rate",
    "fullvaccine_rate",
    "new_booster_first_rate",
    "booster_first_rate"
FROM "opportunity-insights-tracker-covid-city-daily"
