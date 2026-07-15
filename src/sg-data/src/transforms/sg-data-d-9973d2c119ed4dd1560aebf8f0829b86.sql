-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "uen",
    "directory_ref_no",
    "company_name",
    "address",
    "postal_code",
    "email_address",
    "contact_no"
FROM "sg-data-d-9973d2c119ed4dd1560aebf8f0829b86"
