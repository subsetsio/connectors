-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dvs_res_id",
    "_name" AS name,
    "service",
    "phone_number",
    "address",
    "city",
    "state",
    "postcode",
    "borough",
    "email_address",
    "website",
    "service_details",
    "certifications",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "_location" AS location
FROM "nyc-open-data-ybdk-jmnn"
