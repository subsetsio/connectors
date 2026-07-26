-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reporting_year",
    "aggregate_level_citywide_borough_council_district_census_tract",
    "aggregate_level_id",
    "total_storefronts",
    "median_square_feet",
    "average_square_feet",
    "storefront_leased_to_tenants",
    "storefront_reported_occupied_by_owner",
    "storefront_reported_not_leased_and_not_owner_occupied",
    "storefront_under_construction_with_projects_listed",
    "median_years_for_construction_projects",
    "average_years_for_construction_projects"
FROM "nyc-open-data-x3n4-h56k"
