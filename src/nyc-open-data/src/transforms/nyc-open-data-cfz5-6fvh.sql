-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "city_council_district",
    "agency",
    "site",
    "address",
    "borough",
    "disadvantaged_community",
    "installation_date",
    "installed_or_estimated_capacity",
    "percentage_of_max_peak_demand",
    "estimated_annual_production",
    "percentage_of_annual_electricity_consumption",
    "estimated_annual_emissions_reduction",
    "estimated_social_cost_of_carbon_value",
    "estimated_annual_energy_savings",
    "upfront_project_cost",
    "financing_mechanism",
    "status",
    "solarreadiness_assessment",
    "total_gross_square_footage",
    "roof_condition",
    "roof_age",
    "other_sustaibility_projects",
    "year_of_report",
    "data_current_as_of",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-cfz5-6fvh"
