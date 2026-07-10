-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Enrollment ID" AS enrollment_id,
    "National Provider Identifier" AS national_provider_identifier,
    "First Name" AS first_name,
    "Last Name" AS last_name,
    "Organization Name" AS organization_name,
    "Enrollment State Code" AS enrollment_state_code,
    CAST("Enrollment Type" AS BIGINT) AS enrollment_type,
    "Provider Type Text" AS provider_type_text,
    "Enrollment Specialty" AS enrollment_specialty,
    "Revalidation Due Date" AS revalidation_due_date,
    "Adjusted Due Date" AS adjusted_due_date,
    "Individual Total Reassign To" AS individual_total_reassign_to,
    "Receiving Benefits Reassignment" AS receiving_benefits_reassignment
FROM "cms-3746498e-874d-45d8-9c69-68603cafea60"
