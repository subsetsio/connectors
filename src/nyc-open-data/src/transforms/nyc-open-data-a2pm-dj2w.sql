-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "number_of_public_housing_residents_who_passed_the_test_assessing_secondary_completion_tasc",
    "development",
    "number_of_public_housing_residents_who_passed_the_test_assessing_secondary_completion_tasc_1",
    "council_district",
    "number_of_public_housing_residents_who_passed_the_test_assessing_secondary_completion_tasc_2"
FROM "nyc-open-data-a2pm-dj2w"
