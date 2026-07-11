-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "license_type",
    "first_name",
    "last_name",
    CAST("issued_date" AS TIMESTAMP) AS issued_date,
    CAST("expiration_date" AS TIMESTAMP) AS expiration_date,
    "license_status"
FROM "new-york-state-department-of-labor-cxfs-ya8e"
