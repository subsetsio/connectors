-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "waitlist_application_id",
    "record_category",
    "applicant_name",
    "blue_waitlist_number",
    "waitlist_status",
    "selection_date",
    "general_vendor_license_number",
    "general_vendor_license_status",
    "general_vendor_license_type",
    "city",
    "state",
    "zip_code"
FROM "nyc-open-data-r9ax-4va4"
