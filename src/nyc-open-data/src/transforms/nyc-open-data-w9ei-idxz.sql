-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objectid",
    "a",
    "service_category",
    "service_type",
    "walkin",
    "insurance",
    "children",
    "facility_name",
    "address",
    "city",
    "borough",
    "latitude",
    "longitude",
    "zip_code",
    "phone",
    "website",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "more_information",
    "dohmh_website",
    "_location" AS location
FROM "nyc-open-data-w9ei-idxz"
