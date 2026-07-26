-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_name" AS name,
    "address",
    "city",
    "state",
    "postcode",
    "borough",
    "installation",
    "phone",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract",
    "neighborhood_tabulation_area_nta_2020",
    "last_updated_date"
FROM "nyc-open-data-y9b6-624z"
