-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly unemployment insurance rows are program-level claim and payment measures by area and month; claim counts, weeks, benefit amounts, and payments are different measures.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    strptime("Date", '%m/%d/%Y')::DATE AS date,
    CAST("Initial Claims" AS BIGINT) AS initial_claims,
    CAST("First Payments" AS BIGINT) AS first_payments,
    CAST("Weeks Claimed" AS BIGINT) AS weeks_claimed,
    CAST("Weeks Compensated" AS BIGINT) AS weeks_compensated,
    CAST("Average Weekly Benefit*" AS DOUBLE) AS average_weekly_benefit,
    CAST("Benefits Paid" AS DOUBLE) AS benefits_paid,
    CAST("Final Payments" AS BIGINT) AS final_payments
FROM "california-edd-f9d2aa1a-5f94-468d-b5ef-26b3b9418694"
