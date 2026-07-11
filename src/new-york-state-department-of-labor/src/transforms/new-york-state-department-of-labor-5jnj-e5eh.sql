-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "certificate_number",
    "certificate_category",
    "certificate_category_number",
    "first_name",
    "last_name",
    "employer_type",
    "address1",
    "city",
    "state",
    "postal_code",
    CAST("phone" AS BIGINT) AS phone,
    "email_address",
    "service_area",
    CAST("issue_date" AS TIMESTAMP) AS issue_date,
    CAST("expiration_date" AS TIMESTAMP) AS expiration_date,
    "status",
    "georeference",
    "employer_name",
    "address2"
FROM "new-york-state-department-of-labor-5jnj-e5eh"
