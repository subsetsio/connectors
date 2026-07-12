-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source-provided row number column0 is part of the row identity because the table unions multiple UK geography and metric files.
-- caution: Filter to one _source_file before interpreting zip_prediction, lad_code, or measurement_category.
SELECT
    "column0",
    "zip_prediction",
    "user_count",
    "average_support_ratio",
    "ds",
    "_source_file" AS source_file,
    "measurement_category",
    "english_language_ratio",
    "expected_english_language_ratio",
    "average_bias",
    "average_clustering",
    "high_ses_ratio",
    "expected_high_ses_ratio",
    "num_users",
    "volunteering_fraction",
    "activism_fraction",
    "target_age_cohort_ratio",
    "expected_target_age_cohort_ratio",
    "num_volunteering_groups_1000_people_zip",
    "num_activism_groups_1000_people_zip",
    "zip_prediction_full",
    "num_volunteering_groups_1000_people_zip_full",
    "num_activism_groups_1000_people_zip_full",
    "lad_code",
    "num_volunteering_groups_1000_people_lad",
    "num_activism_groups_1000_people_lad"
FROM "meta-uk-social-capital-atlas"
