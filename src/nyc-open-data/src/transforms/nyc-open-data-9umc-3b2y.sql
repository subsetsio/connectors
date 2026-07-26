-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "organization_name",
    "organization_address",
    "city",
    "state",
    "postcode",
    "building_number",
    "school_number",
    "community_board",
    "council_district",
    "project_title",
    "project_description",
    "amnt_requested",
    "funded_amount",
    "borough",
    "latitude",
    "longitude",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-9umc-3b2y"
