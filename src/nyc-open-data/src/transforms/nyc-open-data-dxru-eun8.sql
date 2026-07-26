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
    "storefront_leased_and_not_operating_on_1231",
    "median_monthly_rent_per_square_foot",
    "average_monthly_rent_per_square_foot",
    "median_years_leased",
    "average_years_leased",
    "storefronts_with_leases_ending_after_1231",
    "median_years_lease_term_remaining_after_1231",
    "average_years_lease_term_remaining_after_1231",
    "number_whose_lease_is_due_to_expire_within_the_two_years_after_61",
    "storefront_reported_occupied_by_owner",
    "median_years_occupied_by_owner",
    "average_years_occupied_by_owner",
    "storefront_reported_not_leased_and_not_owner_occupied",
    "median_years_not_leased_and_not_owner_occupied",
    "average_years_not_leased_and_not_owner_occupied",
    "storefront_under_construction_with_dob_projects_listed",
    "median_years_for_construction_projects",
    "average_years_for_construction_projects"
FROM "nyc-open-data-dxru-eun8"
