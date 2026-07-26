-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "american_community_survey_acs_data_time_period",
    "borough",
    "borough_community_district_code",
    "community_district_name",
    "_language" AS language,
    "lep_population_estimate",
    "of_lep_population",
    "cvalep_population_estimate",
    "of_cvalep_population"
FROM "nyc-open-data-ajin-gkbp"
