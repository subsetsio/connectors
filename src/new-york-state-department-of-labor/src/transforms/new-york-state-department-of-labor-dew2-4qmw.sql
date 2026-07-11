-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Funding program rows do not expose a stable non-null identifier, and a program can appear more than once for different funding amounts or sources.
SELECT
    "funding_program_name",
    "total_monetary_amount_of",
    "funding_source",
    "administering_agency",
    "purpose_of_funding_program",
    "website_url",
    "year_program_established",
    "additional_information",
    "federal_domestic_assistance",
    "statute_regulation_that_grants",
    "program_contact_first_name",
    "program_contact_last_name",
    "program_contact_phone_number",
    "program_contact_email",
    "agency_of_program_contact",
    "fiscal_contact_first_name",
    "fiscal_contact_last_name",
    "fiscal_contact_phone_number",
    "fiscal_contact_email",
    "agency_of_fiscal_contact",
    "program_eligibility",
    "program_special_restrictions",
    "action_s_to_receive_aid",
    "description_of_the_aid_flow",
    "second_website_url",
    "funding_source_if_other"
FROM "new-york-state-department-of-labor-dew2-4qmw"
