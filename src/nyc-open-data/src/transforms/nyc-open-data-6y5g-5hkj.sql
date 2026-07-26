-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "waiting_list_application_id",
    "application_order_number",
    "priority_number",
    "applicant_name",
    "city",
    "state",
    "postcode",
    "waiting_list_status",
    "selection_date",
    "license_application_id"
FROM "nyc-open-data-6y5g-5hkj"
