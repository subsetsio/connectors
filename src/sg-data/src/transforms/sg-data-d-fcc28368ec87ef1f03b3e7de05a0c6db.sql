-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Name_of_Caterer" AS name_of_caterer,
    "Contact_Person" AS contact_person,
    "Contact_Number" AS contact_number,
    "Email_Address" AS email_address
FROM "sg-data-d-fcc28368ec87ef1f03b3e7de05a0c6db"
