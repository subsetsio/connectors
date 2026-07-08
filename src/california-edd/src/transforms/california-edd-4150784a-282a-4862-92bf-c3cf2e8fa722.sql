SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Date" AS date,
    "Month" AS month,
    TRY_CAST("Year" AS INTEGER) AS year,
    TRY_CAST(NULLIF(regexp_replace(CAST("Initial Claims Filed" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS initial_claims_filed,
    TRY_CAST(NULLIF(regexp_replace(CAST("Initial Claims Paid" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS initial_claims_paid,
    TRY_CAST(NULLIF(regexp_replace(CAST("Average Weekly Benefit Amount (AWBA)" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS avg_weekly_benefit_amount,
    TRY_CAST(NULLIF(regexp_replace(CAST("Weeks Compensated" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS weeks_compensated,
    TRY_CAST(NULLIF(regexp_replace(CAST("Average Duration" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS average_duration,
    TRY_CAST(NULLIF(regexp_replace(CAST("Total Benefits Authorized" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS total_benefits_authorized,
    TRY_CAST(NULLIF(regexp_replace(CAST("DI Fund Balance" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS di_fund_balance
FROM "california-edd-4150784a-282a-4862-92bf-c3cf2e8fa722"
