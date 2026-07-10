-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: OEWS rows mix geographic, industry, occupation, and wage-type dimensions; filter those dimensions before comparing or aggregating wage measures.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    CAST("Year" AS BIGINT) AS year,
    "Quarter" AS quarter,
    "Industry Name" AS industry_name,
    "Standard Occupational Classification" AS standard_occupational_classification,
    "Occupational Title" AS occupational_title,
    "Wage Type" AS wage_type,
    CAST("Number of Employed" AS BIGINT) AS number_of_employed,
    CAST("Mean Wage" AS DOUBLE) AS mean_wage,
    CAST("10th Percentile Wage" AS DOUBLE) AS "10th_percentile_wage",
    CAST("25th Percentile Wage" AS DOUBLE) AS "25th_percentile_wage",
    CAST("50th Percentile (Median) Wage" AS DOUBLE) AS "50th_percentile_median_wage",
    CAST("75th Percentile Wage" AS DOUBLE) AS "75th_percentile_wage",
    CAST("90th Percentile Wage" AS DOUBLE) AS "90th_percentile_wage",
    CAST("Mean Relative Standard Error for Wage" AS DOUBLE) AS mean_relative_standard_error_for_wage
FROM "california-edd-6411456b-594b-4b73-af57-ce8dd401f2e2"
