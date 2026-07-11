-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study" AS field_of_study,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Science occupations - Total - Number" AS science_occupations_total_number,
    "Science occupations - Total - SE" AS science_occupations_total_se,
    "Science occupations - Post-secondary teachers - Number" AS science_occupations_post_secondary_teachers_number,
    "Science occupations - Post-secondary teachers - SE" AS science_occupations_post_secondary_teachers_se,
    "Science occupations - Other - Number" AS science_occupations_other_number,
    "Science occupations - Other - SE" AS science_occupations_other_se,
    "Engineering occupations - Total - Number" AS engineering_occupations_total_number,
    "Engineering occupations - Total - SE" AS engineering_occupations_total_se,
    "Engineering occupations - Post-secondary teachers - Number" AS engineering_occupations_post_secondary_teachers_number,
    "Engineering occupations - Post-secondary teachers - SE" AS engineering_occupations_post_secondary_teachers_se,
    "Engineering occupations - Other - Number" AS engineering_occupations_other_number,
    "Engineering occupations - Other - SE" AS engineering_occupations_other_se,
    "S and E-related occupations - Total - Number" AS s_and_e_related_occupations_total_number,
    "S and E-related occupations - Total - SE" AS s_and_e_related_occupations_total_se,
    "S and E-related occupations - Health occupations - Number" AS s_and_e_related_occupations_health_occupations_number,
    "S and E-related occupations - Health occupations - SE" AS s_and_e_related_occupations_health_occupations_se,
    "S and E-related occupations - S and E managers - Number" AS s_and_e_related_occupations_s_and_e_managers_number,
    "S and E-related occupations - S and E managers - SE" AS s_and_e_related_occupations_s_and_e_managers_se,
    "S and E-related occupations - Other - Number" AS s_and_e_related_occupations_other_number,
    "S and E-related occupations - Other - SE" AS s_and_e_related_occupations_other_se,
    "Non-S and E occupations - Total - Number" AS non_s_and_e_occupations_total_number,
    "Non-S and E occupations - Total - SE" AS non_s_and_e_occupations_total_se,
    "Non-S and E occupations - Non-S and E managers - Number" AS non_s_and_e_occupations_non_s_and_e_managers_number,
    "Non-S and E occupations - Non-S and E managers - SE" AS non_s_and_e_occupations_non_s_and_e_managers_se,
    "Non-S and E occupations - Non-S and E teachers - Number" AS non_s_and_e_occupations_non_s_and_e_teachers_number,
    "Non-S and E occupations - Non-S and E teachers - SE" AS non_s_and_e_occupations_non_s_and_e_teachers_se,
    "Non-S and E occupations - Other - Number" AS non_s_and_e_occupations_other_number,
    "Non-S and E occupations - Other - SE" AS non_s_and_e_occupations_other_se
FROM "ncses-nsf25321-tab048"
