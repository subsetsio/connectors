-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Regional Planning Unit rows mix areas and occupational classifications; filter area and occupation before aggregating projection measures.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Period" AS period,
    "Standard Occupational Classification (SOC) Code" AS standard_occupational_classification_soc_code,
    "Occupational Title" AS occupational_title,
    "Base Year" AS base_year,
    "Projection Employment Estimate" AS projection_employment_estimate,
    "Numeric Change" AS numeric_change,
    "Percent Change" AS percent_change,
    "Exits" AS exits,
    "Transfers" AS transfers,
    "Total Job Openings" AS total_job_openings,
    "Median Hourly Wage" AS median_hourly_wage,
    "Median Annual Wage" AS median_annual_wage,
    "Entry Level Education" AS entry_level_education,
    "Work Experience" AS work_experience,
    "Job Training" AS job_training
FROM "california-edd-f673ad7c-44ed-4c54-adc7-2f4b23eec557"
