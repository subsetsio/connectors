-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "branches_43",
    "total_r_d_expenditure_in_1000_eur",
    "labour_costs_in_1000_eur",
    "other_current_costs_in_1000_eur",
    "costs_for_instruments_and_equipment_in_1000_eur",
    "costs_for_buildings_and_estates_in_1000_eur",
    "total_intramural_r_d_expendit_in_1000_eur",
    "basic_research_in_1000_eur",
    "basic_research_in_per_cent",
    "applied_research_in_1000_eur",
    "applied_research_in_per_cent",
    "experimental_development_in_1000_eur",
    "experimental_development_in_per_cent",
    "source_of_funds_in_total_in_1000_eur",
    "business_enterprise_sector_in_1000_eur",
    "public_sector_total_in_1000_eur",
    "public_sector_of_which_central_gov_bund_in_1000_eur",
    "public_sector_of_which_local_gov_l_nder_in_1000_eur",
    "publ_s_of_wh_ffg_aust_res_prom_agency_in_1000_eur",
    "public_sector_of_which_other_public_financ_in_1000_eur",
    "private_non_profit_sector_in_1000_eur",
    "other_countries_in_total_in_1000_eur",
    "abroad_of_which_eu_in_1000_eur",
    "other_countries_of_which_others_except_eu_in_1000_eur"
FROM "statistics-austria-ogd-f1830f2009-fue-af1828-2009-1"
