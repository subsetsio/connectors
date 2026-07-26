-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_location" AS location,
    "_name" AS name,
    "license",
    "business_address",
    "city_or_town",
    "state",
    "zip_code",
    "phone_no",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020",
    "effective_date"
FROM "nyc-open-data-f264-qcv3"
