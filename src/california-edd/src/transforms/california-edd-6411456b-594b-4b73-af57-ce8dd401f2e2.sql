SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    TRY_CAST("Year" AS INTEGER) AS year,
    "Quarter" AS quarter,
    "Industry Name" AS industry_name,
    "Standard Occupational Classification" AS soc_code,
    "Occupational Title" AS occupational_title,
    "Wage Type" AS wage_type,
    TRY_CAST(NULLIF(regexp_replace(CAST("Number of Employed" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS number_of_employed,
    TRY_CAST(NULLIF(regexp_replace(CAST("Mean Wage" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS mean_wage,
    TRY_CAST(NULLIF(regexp_replace(CAST("10th Percentile Wage" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS pct10_wage,
    TRY_CAST(NULLIF(regexp_replace(CAST("25th Percentile Wage" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS pct25_wage,
    TRY_CAST(NULLIF(regexp_replace(CAST("50th Percentile (Median) Wage" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS median_wage,
    TRY_CAST(NULLIF(regexp_replace(CAST("75th Percentile Wage" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS pct75_wage,
    TRY_CAST(NULLIF(regexp_replace(CAST("90th Percentile Wage" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS pct90_wage,
    TRY_CAST(NULLIF(regexp_replace(CAST("Mean Relative Standard Error for Wage" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS mean_rse_wage
FROM "california-edd-6411456b-594b-4b73-af57-ce8dd401f2e2"
