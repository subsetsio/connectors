SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Period" AS period,
    "Standard Occupational Classification (SOC) Code" AS soc_code,
    "Occupational Title" AS occupational_title,
    TRY_CAST(NULLIF(regexp_replace(CAST("Base Year" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS base_year_employment,
    TRY_CAST(NULLIF(regexp_replace(CAST("Projection Employment Estimate" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS projected_year_employment,
    TRY_CAST(NULLIF(regexp_replace(CAST("Numeric Change" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS numeric_change,
    TRY_CAST(NULLIF(regexp_replace(CAST("Percent Change" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS percentage_change,
    TRY_CAST(NULLIF(regexp_replace(CAST("Exits" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS exits,
    TRY_CAST(NULLIF(regexp_replace(CAST("Transfers" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS transfers,
    TRY_CAST(NULLIF(regexp_replace(CAST("Total Job Openings" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS total_job_openings,
    TRY_CAST(NULLIF(regexp_replace(CAST("Median Hourly Wage" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS median_hourly_wage,
    TRY_CAST(NULLIF(regexp_replace(CAST("Median Annual Wage" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS median_annual_wage,
    "Entry Level Education" AS entry_level_education,
    "Work Experience" AS work_experience,
    "Job Training" AS job_training
FROM "california-edd-f673ad7c-44ed-4c54-adc7-2f4b23eec557"
