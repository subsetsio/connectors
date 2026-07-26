-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "provider",
    "host_organization",
    "building",
    "street",
    "city",
    "borough",
    "postcode",
    "site_location_address",
    "days_open",
    "_hours" AS hours,
    "languages",
    "telephone",
    "council_district",
    "community_board",
    "bbl",
    "nta",
    "x_coordinates",
    "y_coordinates",
    "latitude",
    "longitude",
    "census_tract",
    "bin",
    "_location" AS location
FROM "nyc-open-data-dt2z-amuf"
