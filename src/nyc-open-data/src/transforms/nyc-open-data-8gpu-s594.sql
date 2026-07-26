-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_number",
    "building_id",
    "project_description",
    "school_name",
    "school_address",
    "sed_approved_estimate",
    "date_application_submitted_to_sed",
    "borough",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "nta_2020"
FROM "nyc-open-data-8gpu-s594"
