-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "svc_request_number",
    "workorder_number",
    "workorder_activity_code",
    "workorder_activity_description",
    "workorder_started",
    "workorder_completed",
    "workorder_added",
    "time_stamp"
FROM "nyc-open-data-4fvw-nn9c"
