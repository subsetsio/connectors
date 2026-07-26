-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "request_id",
    "assigned_agency",
    "request",
    "assigned_agencys_response",
    "request_status",
    "submission_date",
    "legislated_due_date",
    "date_request_closed",
    "data_as_of_date"
FROM "nyc-open-data-63us-eqtq"
