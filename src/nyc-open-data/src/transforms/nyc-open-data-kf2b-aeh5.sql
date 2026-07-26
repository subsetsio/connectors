-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_location" AS location,
    "event_date",
    "check_in_from",
    "check_in_to",
    "event_title",
    "job_family",
    "company_name_or_type",
    "qualifications",
    "borough",
    "location_name_and_address"
FROM "nyc-open-data-kf2b-aeh5"
