-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_location" AS location,
    "request_date",
    "requested_by",
    "type_of_request",
    "request_status",
    "borough"
FROM "nyc-open-data-9a6i-gcns"
