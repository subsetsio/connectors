-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "APM Category" AS apm_category,
    CAST("Total Fee-For-Service Medicare Dollars Paid through APM Category" AS DOUBLE) AS total_fee_for_service_medicare_dollars_paid_through_apm_category,
    CAST("Percent of Fee-For-Service Medicare Dollars Paid through APM Category" AS DOUBLE) AS percent_of_fee_for_service_medicare_dollars_paid_through_apm_category
FROM "cms-7dae1d4a-1e14-4dd5-81b6-ba1dc0509a25"
