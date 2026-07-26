-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "business_name",
    "dbatrade_name",
    "business_unique_id",
    "business_category",
    "license_type",
    "license_status",
    "initial_issuance_date",
    "expiration_date",
    "details",
    "contact_phone",
    "address_type",
    "building_number",
    "street1",
    "street2",
    "street3",
    "unit_type",
    "aptsuite",
    "city",
    "state",
    "zip_code",
    "borough",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "nta",
    "census_block_2010",
    "census_tract_2010",
    "latitude",
    "longitude"
FROM "nyc-open-data-w7w3-xahh"
