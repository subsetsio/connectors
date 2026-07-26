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
    "borough",
    "_location" AS location,
    "forecast_capacity",
    "design_start",
    "construction_start",
    "actual_estcompl",
    "total_est_cost",
    "previous_appropriation",
    "funding_reqd_fy_2024",
    "needed_to_complete",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020",
    "data_as_of"
FROM "nyc-open-data-32rn-zwi7"
