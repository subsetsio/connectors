-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "site_status",
    "site_name",
    "site_number",
    "street_number",
    "street_suffix",
    "street_name",
    "postcode",
    "city",
    "voter_entrance",
    "handicap_entrance",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "_location" AS location
FROM "nyc-open-data-mifw-tguq"
