-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Disability Insurance measures are statewide monthly program totals and include fund-balance measures alongside claim-flow measures.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Date" AS date,
    "Month" AS month,
    CAST("Year" AS BIGINT) AS year,
    "Initial Claims Filed" AS initial_claims_filed,
    "Initial Claims Paid" AS initial_claims_paid,
    "Average Weekly Benefit Amount (AWBA)" AS average_weekly_benefit_amount_awba,
    "Weeks Compensated" AS weeks_compensated,
    CAST("Average Duration" AS DOUBLE) AS average_duration,
    "Total Benefits Authorized" AS total_benefits_authorized,
    "DI Fund Balance" AS di_fund_balance
FROM "california-edd-4150784a-282a-4862-92bf-c3cf2e8fa722"
