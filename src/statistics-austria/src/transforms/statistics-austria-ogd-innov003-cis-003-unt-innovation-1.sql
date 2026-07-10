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
    "innovators_by_type_of_innovation_new_signif_improved_supporting_activities_for_processes",
    "innovators_by_type_of_innovation_new_signif_improved_supporting_activities_for_processes_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_business_practices_for_organising_procedures",
    "innovators_by_type_of_innovation_new_business_practices_for_organising_procedures_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_methods_of_organising_work_responsib_and_decision_making",
    "innovators_by_type_of_innovation_new_methods_of_organising_work_responsib_and_decision_making_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_methods_of_organising_external_relations",
    "innovators_by_type_of_innovation_new_methods_of_organising_external_relations_as_of_all_enterprises",
    "innovators_by_type_of_innovation_significant_changes_to_the_aesthetic_design_or_packaging",
    "innovators_by_type_of_innovation_significant_changes_to_the_aesthetic_design_or_packaging_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_media_or_techniques_for_product_promotion",
    "innovators_by_type_of_innovation_new_media_or_techniques_for_product_promotion_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_methods_for_product_placement_or_sales_channels",
    "innovators_by_type_of_innovation_new_methods_for_product_placement_or_sales_channels_as_of_all_enterprises",
    "innovators_by_type_of_innovation_new_methods_of_pricing_goods_or_services",
    "innovators_by_type_of_innovation_new_methods_of_pricing_goods_or_services_as_of_all_enterprises"
FROM "statistics-austria-ogd-innov003-cis-003-unt-innovation-1"
