-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "building_id",
    "borough",
    "number",
    "street",
    "total_units",
    "program_start_date",
    "current_status",
    "discharge_date",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract_2020",
    "bin",
    "bbl",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-h4mf-f24e"
