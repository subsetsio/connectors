-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objectid",
    "borough",
    "_type" AS type,
    "provider",
    "_name" AS name,
    "_location" AS location,
    "latitude",
    "longitude",
    "x",
    "y",
    "location_t",
    "remarks",
    "city",
    "ssid",
    "sourceid",
    "activated",
    "borocode",
    "borough_name",
    "neighborhood_tabulation_area_code_ntacode",
    "neighborhood_tabulation_area_nta",
    "council_distrcit",
    "postcode",
    "borocd",
    "census_tract",
    "bctcb2010",
    "bin",
    "bbl",
    "doitt_id",
    "location_lat_long"
FROM "nyc-open-data-yjub-udmw"
