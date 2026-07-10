-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "ENROLLMENT ID" AS enrollment_id,
    "ASSOCIATE ID" AS associate_id,
    "ORGANIZATION NAME" AS organization_name,
    "ASSOCIATE ID - OWNER" AS associate_id_owner,
    "TYPE - OWNER" AS type_owner,
    CAST("ROLE CODE - OWNER" AS BIGINT) AS role_code_owner,
    "ROLE TEXT - OWNER" AS role_text_owner,
    "ASSOCIATION DATE - OWNER" AS association_date_owner,
    "FIRST NAME - OWNER" AS first_name_owner,
    "MIDDLE NAME - OWNER" AS middle_name_owner,
    "LAST NAME - OWNER" AS last_name_owner,
    "TITLE - OWNER" AS title_owner,
    "ORGANIZATION NAME - OWNER" AS organization_name_owner,
    "DOING BUSINESS AS NAME - OWNER" AS doing_business_as_name_owner,
    "ADDRESS LINE 1 - OWNER" AS address_line_1_owner,
    "ADDRESS LINE 2 - OWNER" AS address_line_2_owner,
    "CITY - OWNER" AS city_owner,
    "STATE - OWNER" AS state_owner,
    "ZIP CODE - OWNER" AS zip_code_owner,
    "PERCENTAGE OWNERSHIP" AS percentage_ownership,
    "CREATED FOR ACQUISITION - OWNER" AS created_for_acquisition_owner,
    "CORPORATION - OWNER" AS corporation_owner,
    "LLC - OWNER" AS llc_owner,
    "MEDICAL PROVIDER SUPPLIER - OWNER" AS medical_provider_supplier_owner,
    "MANAGEMENT SERVICES COMPANY - OWNER" AS management_services_company_owner,
    "MEDICAL STAFFING COMPANY - OWNER" AS medical_staffing_company_owner,
    "HOLDING COMPANY - OWNER" AS holding_company_owner,
    "INVESTMENT FIRM - OWNER" AS investment_firm_owner,
    "FINANCIAL INSTITUTION - OWNER" AS financial_institution_owner,
    "CONSULTING FIRM - OWNER" AS consulting_firm_owner,
    "FOR PROFIT - OWNER" AS for_profit_owner,
    "NON PROFIT - OWNER" AS non_profit_owner,
    "OTHER TYPE - OWNER" AS other_type_owner,
    "OTHER TYPE TEXT - OWNER" AS other_type_text_owner
FROM "cms-60625dc8-b621-45f0-9423-077fd133b13e"
