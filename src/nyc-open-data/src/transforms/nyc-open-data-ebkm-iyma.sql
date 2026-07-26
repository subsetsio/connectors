-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscalyear",
    "program_area",
    "program_type",
    "service_category",
    "provider",
    "program_site_name",
    "borough",
    "street_address",
    "city",
    "state",
    "postcode",
    "latitude",
    "longitude",
    "x_coordinate",
    "y_coordinate",
    "community_board",
    "community_name",
    "council_district",
    "census_tract_2010",
    "nda",
    "nta",
    "bin",
    "bbl",
    "totalslots",
    "totalparticipants",
    "contract",
    "portfolioid",
    "age_range",
    "_location" AS location
FROM "nyc-open-data-ebkm-iyma"
