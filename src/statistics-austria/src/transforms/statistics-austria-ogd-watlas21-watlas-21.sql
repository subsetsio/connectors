-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_starting_2021" AS BIGINT) AS year_starting_2021,
    "number_of_enterprises_nace_rev_2_g",
    "persons_employed_nace_rev_2_g",
    "employees_nace_rev_2_g",
    "personnel_costs_in_eur_million_nace_rev_2_g",
    "turnover_trade_total_in_eur_million_nace_rev_2_g",
    "turnover_retail_trade_in_eur_million_nace_rev_2",
    "total_purchases_of_goods_and_services_in_eur_million_nace_rev_2_g" AS ttl_prchss_of_gds_and_srvcs_in_er_mlln_nc_rv_2_g,
    "value_added_at_factor_cost_in_eur_million_nace_rev_2_g",
    "gross_investments_in_eur_million_nace_rev_2_g",
    "unemployed_ilo_definition_nace_rev_2_g",
    "total_hours_worked_national_accounts_concept_in_million_hours_nace_rev_2_g" AS ttl_hrs_wrkd_ntnl_accnts_cncpt_in_mlln_hrs_nc_rv_2_g,
    "persons_employed_per_enterprise_nace_rev_2_g",
    "turnover_per_enterprise_in_eur_nace_rev_2_g",
    "turnover_per_person_employed_in_eur_nace_rev_2_g",
    "annual_personnel_expenditure_per_employee_in_eur_nace_rev_2_g",
    "economic_growth_in_industry_nace_rev_2_g_real_in",
    "share_of_enterprises_in_with_broadband_connection_nace_rev_2_g",
    "turnover_index_2021_100_nace_rev_2_g",
    "index_of_number_of_persons_employed_2021_100_nace_rev_2_g",
    "labour_cost_index_2020_100_nace_2008_g",
    "consumption_expenditure_of_households_for_food_in_eur_million",
    "consumption_expenditure_of_households_for_beverage_in_eur_million" AS cnsmptn_expndtr_of_hshlds_fr_bvrg_in_er_mlln,
    "consumption_expenditure_of_households_for_clothing_and_footwear_in_eur_million" AS cnsmptn_expndtr_of_hshlds_fr_clthng_and_ftwr_in_er_mlln,
    "consumption_expenditure_of_households_for_purchase_of_vehicles_in_eur_million" AS cnsmptn_expndtr_of_hshlds_fr_prchs_of_vhcls_in_er_mlln,
    "private_households",
    "wholesale_price_index_2000_100"
FROM "statistics-austria-ogd-watlas21-watlas-21"
