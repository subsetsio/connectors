SELECT
    "Date" AS date,
    "Month" AS month,
    TRY_CAST("Year" AS INTEGER) AS year,
    TRY_CAST(NULLIF(regexp_replace(CAST("Total PFL First Claims Filed" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS total_first_claims_filed,
    TRY_CAST(NULLIF(regexp_replace(CAST("Bonding Claims Filed" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS bonding_claims_filed,
    TRY_CAST(NULLIF(regexp_replace(CAST("Care Claims Filed" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS care_claims_filed,
    TRY_CAST(NULLIF(regexp_replace(CAST("Total PFL First Claims Paid" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS total_first_claims_paid,
    TRY_CAST(NULLIF(regexp_replace(CAST("Bonding Claims Paid" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS bonding_claims_paid,
    TRY_CAST(NULLIF(regexp_replace(CAST("Care Claims Paid" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS care_claims_paid,
    TRY_CAST(NULLIF(regexp_replace(CAST("PFL Average Weekly Benefit Amount (AWBA)" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS avg_weekly_benefit_amount,
    TRY_CAST(NULLIF(regexp_replace(CAST("Weeks Compensated" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS weeks_compensated,
    TRY_CAST(NULLIF(regexp_replace(CAST("Average Duration" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS average_duration,
    TRY_CAST(NULLIF(regexp_replace(CAST("Total Benefits Authorized" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS total_benefits_authorized
FROM "california-edd-3f530a9c-782f-4f34-bf51-9edaa448e0db"
