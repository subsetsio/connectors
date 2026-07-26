-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dca_license_number",
    "license_type",
    "license_creation_date",
    "license_expiration_date",
    "license_status",
    "license_status_date",
    "business_code",
    "business_code_description",
    "business_name",
    "business_name2",
    "address_building",
    "address_street_name",
    "secondary_address_street_name",
    "address_city",
    "address_state",
    "address_postcode",
    "contact_phone_number",
    "borough_code",
    "community_board",
    "council_district",
    "borough",
    "latitude",
    "longitude",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-m4ph-grrm"
