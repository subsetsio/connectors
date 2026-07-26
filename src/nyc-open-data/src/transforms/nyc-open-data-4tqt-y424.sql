-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "vendor_name",
    "type_of_service",
    "active_employees",
    "job_type"
FROM "nyc-open-data-4tqt-y424"
