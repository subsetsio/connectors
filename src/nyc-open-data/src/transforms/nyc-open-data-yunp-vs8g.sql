-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization_city_agency_division_name",
    "street_addressmailing_address",
    "city",
    "state",
    "postcode",
    "year_surveyed",
    "total_vounteers",
    "youth_volunteers",
    "adult_volunteers",
    "older_adult_volunteers",
    "organization_type",
    "interest_areas",
    "special_populations_served",
    "boroughs_served",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-yunp-vs8g"
