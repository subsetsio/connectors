-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "request_id",
    "agency_name",
    "request_created_date",
    "request_submitted_date",
    "request_due_date",
    "submission_method",
    "request_status",
    "request_close_date"
FROM "nyc-open-data-kegn-anvq"
