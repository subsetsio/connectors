-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_name",
    "boroughcode",
    "geographical_district",
    "project_description",
    "construction_award",
    "project_type",
    "building_id",
    "building_address",
    "city",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020",
    "location_1"
FROM "nyc-open-data-8586-3zfm"
