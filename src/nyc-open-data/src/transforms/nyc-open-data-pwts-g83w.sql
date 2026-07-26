-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "facilityname",
    "service_type",
    "address",
    "address_2",
    "borough",
    "zipcode",
    "website",
    "email",
    "contacts_email",
    "secondary_email",
    "organization_phone",
    "contact_phone",
    "latitude",
    "longitude",
    "community_board",
    "city_council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-pwts-g83w"
