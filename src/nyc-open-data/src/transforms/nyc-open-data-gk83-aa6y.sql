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
    "sed_approved_final_cost",
    "date_final_cost_report_submitted_to_sed",
    "borough",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_20102020",
    "neighborhood_tabulation_area_nta_20102020"
FROM "nyc-open-data-gk83-aa6y"
