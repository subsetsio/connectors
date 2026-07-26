-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "filed",
    "application",
    "calendar_number",
    "section",
    "number",
    "street",
    "borough",
    "borough_code",
    "block",
    "lot",
    "zoning_district",
    "community_board",
    "project_description",
    "status",
    "decisions_url",
    "date",
    "postcode",
    "latitude",
    "longitude",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020",
    "location_1"
FROM "nyc-open-data-yvxd-uipr"
