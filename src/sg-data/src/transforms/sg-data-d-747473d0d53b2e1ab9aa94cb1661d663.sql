-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RPFE_Authorisation_No" AS rpfe_authorisation_no,
    "RFPE_Name" AS rfpe_name,
    "Ref_No" AS ref_no,
    "RFPE_Branch" AS rfpe_branch,
    "RFPE_Validity_Period" AS rfpe_validity_period,
    "ACPE_Reg_No" AS acpe_reg_no,
    "RFPE_Practice_Name" AS rfpe_practice_name,
    "RFPE_Practice_Address" AS rfpe_practice_address,
    "RFPE_Contact_No" AS rfpe_contact_no,
    "PE_Reg_No" AS pe_reg_no,
    "PE_Name" AS pe_name,
    "PE_Branch" AS pe_branch,
    "PE_Date_of_Reg" AS pe_date_of_reg,
    "PE_Practice_Name" AS pe_practice_name,
    "PE_Practice_Employer_Type" AS pe_practice_employer_type,
    "PE_Practice_Employer_Address" AS pe_practice_employer_address,
    "PE_Contact_No" AS pe_contact_no
FROM "sg-data-d-747473d0d53b2e1ab9aa94cb1661d663"
