-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "address",
    "building",
    "court",
    "total_sq_ft",
    "ct_sq_ft",
    "ct",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "_location" AS location
FROM "nyc-open-data-xx2p-4jnq"
