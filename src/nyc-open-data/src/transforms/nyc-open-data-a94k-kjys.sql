-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sited",
    "leased",
    "district",
    "project",
    "school",
    "boro",
    "forecast_capacity",
    "d75_capacity",
    "design_start",
    "construction_start",
    "actual_est_comp",
    "total_est_comp",
    "previous_appropriations",
    "funding_reqd_fy_2529",
    "needed_to_complete",
    "address",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-a94k-kjys"
