-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "certificate_number",
    "business_name",
    "dba_name",
    "business_type",
    "business_is_mwbe_owned",
    "business_is_publicly_traded",
    "address",
    "city",
    "state",
    "zip_code",
    CAST("phone" AS BIGINT) AS phone,
    CAST("issued_date" AS TIMESTAMP) AS issued_date,
    CAST("expiration_date" AS TIMESTAMP) AS expiration_date,
    "status",
    "business_has_a_nys_dol_employer_registration_number",
    "business_has_a_wcb_employer_number",
    "business_has_outstanding_wage_assessments",
    "business_has_been_debarred",
    "business_has_final_determination_for_violation_of_labor_or_tax_law",
    "business_has_final_determination_safety_standard_violations",
    "business_is_associated_with_an_apprenticeship_program",
    "business_is_sponsor_of_a_program_" AS business_is_sponsor_of_a_program,
    "business_is_signatory_to_a_group_program",
    "business_has_workers_compensation_insurance",
    "business_is_exempt_from_workers_compensation_insurance_" AS business_is_exempt_from_workers_compensation_insurance,
    "georeference",
    "reason_business_does_not_have_a_nys_dol_employer_registration_number_" AS reason_business_does_not_have_a_nys_dol_employer_registration_number,
    "address_2",
    "business_officers",
    "debarment_state_or_federal_law",
    "debarment_state",
    CAST("debarment_start_date" AS TIMESTAMP) AS debarment_start_date,
    CAST("debarment_end_date" AS TIMESTAMP) AS debarment_end_date
FROM "new-york-state-department-of-labor-i4jv-zkey"
