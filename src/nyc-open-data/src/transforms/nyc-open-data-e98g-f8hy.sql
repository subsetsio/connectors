-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permit_bin",
    "permit_application_job_number",
    "permit_application_document_number",
    "permit_application_job_type",
    "permit_type",
    "permit_subtype",
    "permit_status_description",
    "permit_sequence_number",
    "permit_status_date",
    "permit_issuance_date",
    "permit_experation_date"
FROM "nyc-open-data-e98g-f8hy"
