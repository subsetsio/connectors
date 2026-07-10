-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_starting_2021" AS BIGINT) AS year_starting_2021,
    "number_of_enterprises_nace_rev_2_f",
    "persons_employed_nace_rev_2_f",
    "employees_nace_rev_2_f",
    "personnel_costs_in_eur_million_nace_rev_2_f",
    "turnover_in_eur_million_nace_rev_2_f",
    "total_purchases_of_goods_and_services_in_eur_million_nace_rev_2_f",
    "value_added_at_factor_cost_in_eur_million_nace_rev_2_f",
    "gross_investments_in_eur_million_nace_rev_2_f",
    "unemployed_ilo_definition_nace_rev_2_f",
    "total_hours_worked_national_accounts_concept_in_million_hours_nace_rev_2_f",
    "persons_employed_per_enterprise_nace_rev_2_f",
    "turnover_per_enterprise_in_eur_nace_rev_2_f",
    "turnover_per_person_employed_in_eur_nace_rev_2_f",
    "annual_personnel_expenditure_per_employee_in_eur_nace_rev_2_f",
    "economic_growth_in_industry_nace_rev_2_f_real_in",
    "intensity_of_export_in_nace_rev_2_f",
    "share_of_enterprises_in_with_broadband_connection_nace_rev_2_f",
    "turnover_index_2021_100_nace_rev_2_f",
    "production_index_wd_adjusted_2021_100_nace_rev_2_f",
    "new_orders_index_2021_100_nace_rev_2_f",
    "index_of_persons_employed_2021_100_nace_rev_2_f",
    "index_of_hours_worked_2021_100_nace_rev_2_f",
    "labour_cost_index_2020_100_nace_2008_f",
    "construction_output_price_index_for_building_construction_and_civil_engineering_2010_100",
    "construction_cost_index_for_construction_of_residential_buildings_2010_100"
FROM "statistics-austria-ogd-watlas20-watlas-20"
