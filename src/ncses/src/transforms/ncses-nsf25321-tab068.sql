-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation" AS occupation,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "≤ 5 - Median salary" AS 5_median_salary,
    "≤ 5 - SE" AS 5_se,
    "6–10 - Median salary" AS 6_10_median_salary,
    "6–10 - SE" AS 6_10_se,
    "11–15 - Median salary" AS 11_15_median_salary,
    "11–15 - SE" AS 11_15_se,
    "16–20 - Median salary" AS 16_20_median_salary,
    "16–20 - SE" AS 16_20_se,
    "21–25 - Median salary" AS 21_25_median_salary,
    "21–25 - SE" AS 21_25_se,
    "> 25 - Median salary" AS 25_median_salary,
    "> 25 - SE" AS 25_se
FROM "ncses-nsf25321-tab068"
