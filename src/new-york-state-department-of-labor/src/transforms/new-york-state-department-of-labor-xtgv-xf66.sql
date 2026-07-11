-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "certificate_number",
    "business_name",
    "address1",
    "address2",
    "city",
    "state",
    "zip_code",
    CAST("phone" AS BIGINT) AS phone,
    CAST("issue_date" AS TIMESTAMP) AS issue_date,
    CAST("expiration_date" AS TIMESTAMP) AS expiration_date,
    "status"
FROM "new-york-state-department-of-labor-xtgv-xf66"
