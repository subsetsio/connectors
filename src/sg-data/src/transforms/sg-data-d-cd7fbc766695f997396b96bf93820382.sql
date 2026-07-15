-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Company_Name" AS company_name,
    "Contact_Person" AS contact_person,
    "Job_Title" AS job_title,
    "Contact_Number" AS contact_number,
    "Email_Address" AS email_address,
    "Products" AS products,
    "Category" AS category
FROM "sg-data-d-cd7fbc766695f997396b96bf93820382"
