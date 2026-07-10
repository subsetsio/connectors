SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    TRY_CAST("Year" AS INTEGER) AS year,
    COALESCE("Quarter", "Time Period") AS quarter,
    "Ownership" AS ownership,
    "NAICS Level" AS naics_level,
    "NAICS Code" AS naics_code,
    "Industry Name" AS industry_name,
    TRY_CAST(NULLIF(regexp_replace(CAST("Establishments" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS establishments,
    TRY_CAST(NULLIF(regexp_replace(CAST("Average Monthly Employment" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS average_monthly_employment,
    TRY_CAST(NULLIF(regexp_replace(CAST("1st Month Emp" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS first_month_emp,
    TRY_CAST(NULLIF(regexp_replace(CAST("2nd Month Emp" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS second_month_emp,
    TRY_CAST(NULLIF(regexp_replace(CAST("3rd Month Emp" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS third_month_emp,
    TRY_CAST(NULLIF(regexp_replace(CAST("Total Wages (All Workers)" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS total_wages,
    TRY_CAST(NULLIF(regexp_replace(CAST("Average Weekly Wages" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS average_weekly_wages
FROM "california-edd-3f08b68e-1d1a-4ba4-a07d-1ec3392ed191"
