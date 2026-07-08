SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Period" AS period,
    "NAICS Level" AS naics_level,
    "NAICS Code" AS naics_code,
    "Industry Title" AS industry_title,
    TRY_CAST(NULLIF(regexp_replace(CAST("Base Year Employment Estimate" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS base_year_employment,
    TRY_CAST(NULLIF(regexp_replace(CAST("Projected Year Employment Estimate" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS projected_year_employment,
    TRY_CAST(NULLIF(regexp_replace(CAST("Numeric Change" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS numeric_change,
    TRY_CAST(NULLIF(regexp_replace(CAST("Percentage Change" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS percentage_change
FROM "california-edd-b1ac39b1-33cc-4577-b584-6259406ce835"
