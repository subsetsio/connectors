-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "american_community_survey_acs_data_time_period",
    "borough",
    "borough_community_district_code",
    "community_district_name",
    "community_district_population",
    "total_lep_population_estimate",
    "of_population_that_is_lep",
    "total_cvalep_population_estimate",
    "of_population_that_is_cvalep"
FROM "nyc-open-data-9ji4-nien"
