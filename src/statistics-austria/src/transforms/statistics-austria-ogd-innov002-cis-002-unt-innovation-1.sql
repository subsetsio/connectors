-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "industries_nace_and_size_classes",
    "enterprises_with_innovation_cooperation_total",
    "enterprises_with_innovation_cooperation_as_of_all_enterp_with_innov_coop",
    "enterprises_with_innovation_cooperation_of_which_other_enterp_within_the_enterpr_group",
    "enterprises_with_innovation_cooperation_of_which_other_enterp_within_the_enterpr_group_as_of_all_enterpr_with_innov_coop",
    "enterprises_with_innovation_cooperation_of_which_suppliers",
    "enterprises_with_innovation_cooperation_of_which_supliers_as_of_all_enterpr_with_innov_coop",
    "enterprises_with_innovation_cooperation_of_which_clients_from_the_private_sector",
    "enterprises_with_innovation_cooperation_of_which_clients_from_the_private_sector_as_of_all_enterpr_with_innov_coop",
    "enterprises_with_innovation_cooperation_of_which_clients_from_the_public_sector",
    "enterprises_with_innovation_cooperation_of_which_clients_from_the_public_sector_as_of_all_enterpr_with_innov_coop",
    "enterprises_with_innovation_cooperation_of_which_competitors",
    "enterprises_with_innovation_cooperation_of_which_competitors_as_of_all_enterpr_with_innov_coop",
    "enterprises_with_innovation_cooperation_of_which_consultants_or_commercial_labs",
    "enterprises_with_innovation_cooperation_of_which_consultants_or_commercial_labs_as_of_all_enterpr_with_innov_coop",
    "enterprises_with_innovation_cooperation_of_which_universities_or_other_higher_education_inst",
    "enterprises_with_innovation_cooperation_of_which_universities_or_other_higher_education_inst_as_of_all_enterpr_with_innov_coop",
    "enterprises_with_innovation_cooperation_of_which_governm_public_o_private_research_inst",
    "enterprises_with_innovation_cooperation_of_which_governm_public_o_private_research_inst_as_of_all_enterpr_with_innov_coop",
    "enterprises_with_innovation_cooperation_of_which_coop_partner_from_austria"
FROM "statistics-austria-ogd-innov002-cis-002-unt-innovation-1"
