-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "jur_dist",
    "bldg_id",
    "building_name",
    "building_address",
    "no_of_tcus",
    "enrollment",
    "council_district",
    "borough",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020",
    "data_as_of"
FROM "nyc-open-data-3spy-rjpw"
