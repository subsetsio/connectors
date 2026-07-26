-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cable_provider_name",
    "street_address",
    "city_state_zip",
    "phone",
    "fax",
    "web_site",
    "_comments" AS comments,
    "borough",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-48pb-zy2g"
