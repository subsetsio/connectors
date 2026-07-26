-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "eo50_approval_date",
    "business_name",
    "business_address",
    "business_city",
    "business_state",
    "business_phone",
    "postcode",
    "borough",
    "community_board",
    "latitude",
    "longitude",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-9a87-6m4x"
