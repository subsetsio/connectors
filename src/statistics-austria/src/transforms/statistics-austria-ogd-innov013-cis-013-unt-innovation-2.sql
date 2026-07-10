-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "industries_nace_and_size_classes",
    "all_enterprises",
    "innovators_by_type_of_innovation_new_goods",
    "innovators_by_type_of_innovation_new_goods_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_services",
    "innovators_by_type_of_innovation_new_services_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_signif_improved_meth_of_manufacturing_f_goods_and_services",
    "innovators_by_type_of_innovation_new_sign_improved_meth_of_manufacturing_f_goods_and_services_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_signif_improved_logistics_delivery_methods",
    "innovators_by_type_of_innovation_new_signif_improved_logistics_delivery_methods_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_signif_improved_supporting_activities_for_dissemination_or_communication",
    "innovators_by_type_of_innovation_new_signif_improved_supporting_activities_for_dissemination_or_communication_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_business_practices_for_accounts_or_administration_procedures",
    "innovators_by_type_of_innovation_new_business_practices_for_accounts_or_administration_procedures_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_methods_of_organising_new_business_practices_or_external_relations",
    "innovators_by_type_of_innovation_new_methods_of_organising_new_business_practices_or_external_relations_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_methods_of_organising_work_responsib_or_decision_making",
    "innovators_by_type_of_innovation_new_methods_of_organising_work_responsib_or_decision_making_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_signif_methods_of_marketing",
    "innovators_by_type_of_innovation_new_signif_methods_of_marketing_as_of_all_enterprises",
    "innovators_by_type_of_innovation_product_innovations",
    "innovators_by_type_of_innovation_product_innovations_as_of_all_enterprises",
    "innovators_by_type_of_innovation_business_process_innovations",
    "innovators_by_type_of_innovation_business_process_innovations_as_of_all_enterprises"
FROM "statistics-austria-ogd-innov013-cis-013-unt-innovation-2"
