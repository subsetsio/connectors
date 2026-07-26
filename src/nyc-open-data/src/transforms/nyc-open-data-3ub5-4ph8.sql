-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "development",
    "tds",
    "building",
    "stairhall",
    "borough",
    "house",
    "street",
    "address",
    "city",
    "state",
    "zip_code",
    "bin",
    "block",
    "lot",
    "boroughblocklot",
    "census_tract_2020",
    "neighborhood_tabulation_area_code",
    "neighborhood_tabulation_area_name",
    "community_district",
    "city_council_district",
    "state_assembly_district",
    "state_senate_district",
    "us_congressional_district",
    "privately_managed",
    "latitude",
    "longitude"
FROM "nyc-open-data-3ub5-4ph8"
