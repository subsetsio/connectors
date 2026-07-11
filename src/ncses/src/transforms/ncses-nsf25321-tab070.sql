-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation" AS occupation,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "With disability - Median salary" AS with_disability_median_salary,
    "With disability - SE" AS with_disability_se,
    "Without disability - Median salary" AS without_disability_median_salary,
    "Without disability - SE" AS without_disability_se
FROM "ncses-nsf25321-tab070"
