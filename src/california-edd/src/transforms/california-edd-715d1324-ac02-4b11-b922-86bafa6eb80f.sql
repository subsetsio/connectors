-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long-term occupational projections mix areas and occupation hierarchy levels; filter area and SOC level before aggregating employment or openings.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Period" AS period,
    CAST("SOC Level" AS BIGINT) AS soc_level,
    "Standard Occupational Classification (SOC)" AS standard_occupational_classification_soc,
    "Occupational Title" AS occupational_title,
    CAST("Base Year Employment Estimate" AS BIGINT) AS base_year_employment_estimate,
    CAST("Projected Year Employment Estimate" AS BIGINT) AS projected_year_employment_estimate,
    CAST("Numeric Change" AS BIGINT) AS numeric_change,
    CAST("Percentage Change" AS DOUBLE) AS percentage_change,
    CAST("Exits" AS BIGINT) AS exits,
    CAST("Transfers" AS BIGINT) AS transfers,
    CAST("Total Job Openings" AS BIGINT) AS total_job_openings,
    CAST("Median Hourly Wage" AS DOUBLE) AS median_hourly_wage,
    CAST("Median Annual Wage" AS BIGINT) AS median_annual_wage,
    "Entry Level Education" AS entry_level_education,
    "Work Experience" AS work_experience,
    "Job Training" AS job_training
FROM "california-edd-715d1324-ac02-4b11-b922-86bafa6eb80f"
