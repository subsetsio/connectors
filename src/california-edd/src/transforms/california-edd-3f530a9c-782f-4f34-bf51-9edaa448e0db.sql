-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Paid Family Leave measures are statewide monthly program totals and should not be combined with disability or unemployment insurance program tables as if they shared the same population.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Date" AS date,
    "Month" AS month,
    CAST("Year" AS BIGINT) AS year,
    "Total PFL First Claims Filed" AS total_pfl_first_claims_filed,
    "Bonding Claims Filed" AS bonding_claims_filed,
    "Care Claims Filed" AS care_claims_filed,
    "Total PFL First Claims Paid" AS total_pfl_first_claims_paid,
    "Bonding Claims Paid" AS bonding_claims_paid,
    "Care Claims Paid" AS care_claims_paid,
    "PFL Average Weekly Benefit Amount (AWBA)" AS pfl_average_weekly_benefit_amount_awba,
    "Weeks Compensated" AS weeks_compensated,
    "Average Duration" AS average_duration,
    "Total Benefits Authorized" AS total_benefits_authorized
FROM "california-edd-3f530a9c-782f-4f34-bf51-9edaa448e0db"
