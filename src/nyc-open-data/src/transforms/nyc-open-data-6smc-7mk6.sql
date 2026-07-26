-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_name" AS name,
    "_hours" AS hours,
    "number",
    "street",
    "street_address_2",
    "city",
    "borough",
    "state",
    "postcode",
    "details",
    "location_type",
    "latitude",
    "longitude",
    "bin",
    "bbl",
    "nta",
    "council_district",
    "census_tract",
    "community_board"
FROM "nyc-open-data-6smc-7mk6"
