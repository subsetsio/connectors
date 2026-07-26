-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "organization",
    "_type" AS type,
    "purpose",
    "funding",
    "project_location",
    "postcode",
    "school_district",
    "council_district",
    "community_board",
    "state_assembly_district",
    "state_senate_district",
    "congressional_district",
    "borough",
    "latitude",
    "longitude",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-mdgu-ar69"
