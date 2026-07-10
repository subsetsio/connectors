-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Case_ID" AS BIGINT) AS case_id,
    "Hosp_Name" AS hosp_name,
    "Hosp_Address" AS hosp_address,
    "City" AS city,
    "State" AS state,
    "Action" AS action,
    "Date_of_Action" AS date_of_action
FROM "cms-6a3aa708-3c9d-411a-a1a4-e046d3ade7ef"
