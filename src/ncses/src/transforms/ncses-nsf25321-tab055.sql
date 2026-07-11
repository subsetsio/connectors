-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Employment sector and field of study" AS employment_sector_and_field_of_study,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "Male - Median salary" AS male_median_salary,
    "Male - SE" AS male_se,
    "Female - Median salary" AS female_median_salary,
    "Female - SE" AS female_se
FROM "ncses-nsf25321-tab055"
