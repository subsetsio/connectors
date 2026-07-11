-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study and sex" AS field_of_study_and_sex,
    "All full-time employed - < 10 - Median salary" AS all_full_time_employed_10_median_salary,
    "All full-time employed - < 10 - SE" AS all_full_time_employed_10_se,
    "All full-time employed - ≥ 10 - Median salary" AS all_full_time_employed_10_median_salary_2,
    "All full-time employed - ≥ 10 - SE" AS all_full_time_employed_10_se_2,
    "Tenured - < 10 - Median salary" AS tenured_10_median_salary,
    "Tenured - < 10 - SE" AS tenured_10_se,
    "Tenured - ≥ 10 - Median salary" AS tenured_10_median_salary_2,
    "Tenured - ≥ 10 - SE" AS tenured_10_se_2,
    "Not tenured - On tenure track - < 10 - Median salary" AS not_tenured_on_tenure_track_10_median_salary,
    "Not tenured - On tenure track - < 10 - SE" AS not_tenured_on_tenure_track_10_se,
    "Not tenured - On tenure track - ≥ 10 - Median salary" AS not_tenured_on_tenure_track_10_median_salary_2,
    "Not tenured - On tenure track - ≥ 10 - SE" AS not_tenured_on_tenure_track_10_se_2,
    "Not tenured - Not on tenure track - < 10 - Median salary" AS not_tenured_not_on_tenure_track_10_median_salary,
    "Not tenured - Not on tenure track - < 10 - SE" AS not_tenured_not_on_tenure_track_10_se,
    "Not tenured - Not on tenure track - ≥ 10 - Median salary" AS not_tenured_not_on_tenure_track_10_median_salary_2,
    "Not tenured - Not on tenure track - ≥ 10 - SE" AS not_tenured_not_on_tenure_track_10_se_2,
    "Tenure not applicable - Not on tenure track - < 10 - Median salary" AS tenure_not_applicable_not_on_tenure_track_10_median_salary,
    "Tenure not applicable - Not on tenure track - < 10 - SE" AS tenure_not_applicable_not_on_tenure_track_10_se,
    "Tenure not applicable - Not on tenure track - ≥ 10 - Median salary" AS tenure_not_applicable_not_on_tenure_track_10_median_salary_2,
    "Tenure not applicable - Not on tenure track - ≥ 10 - SE" AS tenure_not_applicable_not_on_tenure_track_10_se_2
FROM "ncses-nsf25321-tab063"
