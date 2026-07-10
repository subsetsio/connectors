-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "Ind_PAC_ID" AS ind_pac_id,
    "Provider Last Name" AS provider_last_name,
    "Provider First Name" AS provider_first_name,
    "Provider Middle Name" AS provider_middle_name,
    "suff",
    "facility_type",
    "Facility Affiliations Certification Number" AS facility_affiliations_certification_number,
    "Facility Type Certification Number" AS facility_type_certification_number
FROM "cms-27ea-46a8"
