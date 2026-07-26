-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record",
    "intake_date",
    "service_request_category",
    "service_request_sub_category",
    "date_of_service_request",
    "affilation",
    "branch_of_service",
    "city",
    "state",
    "zip_code",
    "actual_move_out_date",
    "homelessness_status",
    "referred_to",
    "service_request_resolution",
    "service_request_resolution_date"
FROM "nyc-open-data-davn-rbxj"
