-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "certificate_number",
    "business_name",
    CAST("phone" AS BIGINT) AS phone,
    "address1",
    "address2",
    "city",
    "state",
    CAST("zip_code" AS BIGINT) AS zip_code,
    "model_management_business_type",
    CAST("issue_date" AS TIMESTAMP) AS issue_date,
    CAST("expiration_date" AS TIMESTAMP) AS expiration_date,
    "status",
    "dba",
    "group_companies",
    "group_locations",
    "additional_locations"
FROM "new-york-state-department-of-labor-hder-iq9y"
