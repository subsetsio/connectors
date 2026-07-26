-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_sl_no",
    "license_type",
    "license_number",
    "last_name",
    "first_name",
    "business_name",
    "number",
    "street",
    "license_business_city",
    "business_state",
    "postcode",
    "business_email",
    "business_phone_number",
    "license_status",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-t8hj-ruu2"
