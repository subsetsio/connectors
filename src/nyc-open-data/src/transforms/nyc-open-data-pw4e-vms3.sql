-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "originating_provider_name",
    "case_status",
    "started_as_assistance_request",
    "case_is_referred",
    "service_type",
    "service_subtype",
    "outcome_description",
    "outcome_resolution_type"
FROM "nyc-open-data-pw4e-vms3"
