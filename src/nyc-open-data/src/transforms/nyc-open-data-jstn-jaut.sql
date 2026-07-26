-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "date_issued",
    "recommendation",
    "acceptance_status",
    "implementation_status",
    "date_implemented",
    "agency_reported_status"
FROM "nyc-open-data-jstn-jaut"
