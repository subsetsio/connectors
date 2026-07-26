-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "filing_due_date",
    "reporting_year",
    "borough_block_lot",
    "property_street_address_or_storefront_address",
    "borough",
    "zip_code",
    "sold_date",
    "vacant_on_1231",
    "construction_reported",
    "vacant_630_or_date_sold",
    "primary_business_activity",
    "expiration_date_of_the_most_recent_lease",
    "property_number",
    "property_street",
    "unit",
    "borough1",
    "postcode",
    "latitude",
    "longitude",
    "latlong",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "nta_neighborhood"
FROM "nyc-open-data-92iy-9c3n"
