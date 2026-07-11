-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field of study" AS field_of_study,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "Under 35 - Median salary" AS under_35_median_salary,
    "Under 35 - SE" AS under_35_se,
    "35–39 - Median salary" AS "35_39_median_salary",
    "35–39 - SE" AS "35_39_se",
    "40–44 - Median salary" AS "40_44_median_salary",
    "40–44 - SE" AS "40_44_se",
    "45–49 - Median salary" AS "45_49_median_salary",
    "45–49 - SE" AS "45_49_se",
    "50–54 - Median salary" AS "50_54_median_salary",
    "50–54 - SE" AS "50_54_se",
    "55–59 - Median salary" AS "55_59_median_salary",
    "55–59 - SE" AS "55_59_se",
    "60–64 - Median salary" AS "60_64_median_salary",
    "60–64 - SE" AS "60_64_se",
    "65–75 - Median salary" AS "65_75_median_salary",
    "65–75 - SE" AS "65_75_se"
FROM "ncses-nsf25321-tab052"
