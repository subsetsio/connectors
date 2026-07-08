SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Date" AS date,
    TRY_CAST(NULLIF(regexp_replace(CAST("Initial Claims" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS initial_claims,
    TRY_CAST(NULLIF(regexp_replace(CAST("First Payments" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS first_payments,
    TRY_CAST(NULLIF(regexp_replace(CAST("Weeks Claimed" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS weeks_claimed,
    TRY_CAST(NULLIF(regexp_replace(CAST("Weeks Compensated" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS weeks_compensated,
    TRY_CAST(NULLIF(regexp_replace(CAST("Average Weekly Benefit*" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS average_weekly_benefit,
    TRY_CAST(NULLIF(regexp_replace(CAST("Benefits Paid" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS benefits_paid,
    TRY_CAST(NULLIF(regexp_replace(CAST("Final Payments" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS final_payments
FROM "california-edd-f9d2aa1a-5f94-468d-b5ef-26b3b9418694"
