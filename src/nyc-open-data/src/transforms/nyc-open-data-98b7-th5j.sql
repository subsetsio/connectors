-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_location" AS location,
    "_name" AS name,
    "license_no",
    "business_address",
    "borough",
    "city_or_town",
    "state",
    "community_board",
    "zip_code",
    "phone_no",
    "latitude",
    "longitude",
    "council_district",
    "census_tract_2020",
    "bin",
    "bbl",
    "neighborhood_tabulation_area_nta_2020",
    "effective_date"
FROM "nyc-open-data-98b7-th5j"
