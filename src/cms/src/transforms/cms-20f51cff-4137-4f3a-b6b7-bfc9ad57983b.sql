-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Group PAC ID" AS BIGINT) AS group_pac_id,
    "Group Enrollment ID" AS group_enrollment_id,
    "Group Legal Business Name" AS group_legal_business_name,
    "Group State Code" AS group_state_code,
    "Group Due Date" AS group_due_date,
    CAST("Group Reassignments and Physician Assistants" AS BIGINT) AS group_reassignments_and_physician_assistants,
    "Record Type" AS record_type,
    CAST("Individual PAC ID" AS BIGINT) AS individual_pac_id,
    "Individual Enrollment ID" AS individual_enrollment_id,
    "Individual NPI" AS individual_npi,
    "Individual First Name" AS individual_first_name,
    "Individual Last Name" AS individual_last_name,
    "Individual State Code" AS individual_state_code,
    "Individual Specialty Description" AS individual_specialty_description,
    "Individual Due Date" AS individual_due_date,
    CAST("Individual Total Employer Associations" AS BIGINT) AS individual_total_employer_associations
FROM "cms-20f51cff-4137-4f3a-b6b7-bfc9ad57983b"
