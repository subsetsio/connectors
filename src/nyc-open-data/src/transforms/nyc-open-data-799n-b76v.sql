-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "business_organization",
    "business_type_other",
    "company_name",
    "company_description",
    "organization_location",
    "street_address",
    "apt_number",
    "borough",
    "postcode",
    "business_phone",
    "contact_name",
    "contact_title",
    "contact_phone",
    "contact_fax",
    "_location" AS location,
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-799n-b76v"
