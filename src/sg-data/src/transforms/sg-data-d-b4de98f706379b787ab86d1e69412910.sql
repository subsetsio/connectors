-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "class_of_waste",
    "Licensee_Name" AS licensee_name,
    "Address" AS address,
    "Email_Address" AS email_address,
    "Contact_No" AS contact_no
FROM "sg-data-d-b4de98f706379b787ab86d1e69412910"
