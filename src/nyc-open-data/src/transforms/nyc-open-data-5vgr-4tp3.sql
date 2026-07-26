-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "date",
    "rent_arrears_total_requests",
    "rent_arrears_requests_accepted",
    "rent_arrears_requests_rejected",
    "utilities_total_requests",
    "utilities_total_requests_accepted",
    "utilities_requests_rejected",
    "other_housing_total_requests",
    "other_housing_requests_accepted",
    "other_housing_requests_rejected",
    "storage_total_requests",
    "storage_requests_accepted",
    "storage_requests_rejected",
    "disaster_total_requests",
    "disaster_requests_accepted",
    "disaster_requests_rejected",
    "other_requests_total_requests",
    "other_requests_accepted",
    "other_requests_rejected",
    "total_requests",
    "total_requests_accepted",
    "total_requests_rejected"
FROM "nyc-open-data-5vgr-4tp3"
