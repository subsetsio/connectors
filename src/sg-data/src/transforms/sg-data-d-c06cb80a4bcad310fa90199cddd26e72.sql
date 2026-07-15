-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Organisation_Company" AS organisation_company,
    "Business_GST_Registration_No" AS business_gst_registration_no,
    "Company_URL" AS company_url,
    "Organisation_Type" AS organisation_type,
    "Name" AS name,
    "Email" AS email,
    "Contact_No" AS contact_no
FROM "sg-data-d-c06cb80a4bcad310fa90199cddd26e72"
