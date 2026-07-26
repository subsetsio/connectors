-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_period",
    "report_update_frequency",
    "category",
    "total",
    "of_foster_population",
    "age_group_7_years_old",
    "age_group_7_years_old_of_foster_population",
    "age_group_712_years_old",
    "age_group_712_years_old_of_foster_population",
    "age_group_1317_years_old",
    "age_group_1317_years_old_of_foster_population",
    "female",
    "female_of_foster_population",
    "male",
    "male_of_foster_population"
FROM "nyc-open-data-qw7r-btyb"
