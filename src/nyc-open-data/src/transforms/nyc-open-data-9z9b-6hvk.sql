-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_business",
    "business_type_other",
    "company_name",
    "company_description",
    "street_address",
    "apt_number",
    "borough",
    "postcode",
    "business_phone",
    "contact_name",
    "contact_title",
    "contact_phone",
    "contact_fax",
    "location_1",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-9z9b-6hvk"
