-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "industries_nace_and_size_classes",
    "all_enterprises_with_technological_innovations",
    "enterprises_with_technological_innovations_in_house_r_d",
    "enterprises_with_technological_innovations_in_house_r_d_as_of_all_enterprises",
    "enterprises_with_technological_innovations_external_r_d",
    "enterprises_with_technological_innovations_external_r_d_as_of_all_enterprises",
    "enterprises_with_technological_innovations_acquisition_of_machinery_equipment",
    "enterprises_with_technological_innovations_acquisition_of_machinery_equipment_as_of_all_enterprises",
    "enterprises_with_technological_innovations_acquisition_of_external_knowledge",
    "enterprises_with_technological_innovations_acquisition_of_external_knowledge_as_of_all_enterprises",
    "enterprises_with_technological_innovations_training_for_innovative_activities",
    "enterprises_with_technological_innovations_training_for_innovative_activities_as_of_all_enterprises",
    "enterprises_with_technological_innovations_market_introduction_of_innovations",
    "enterprises_with_technological_innovations_market_introduction_of_innovations_as_of_all_enterprises",
    "enterprises_with_technological_innovations_design",
    "enterprises_with_technological_innovations_design_as_of_all_enterprises",
    "enterprises_with_technological_innovations_other_innov_activities",
    "enterprises_with_technological_innovations_other_innov_activities_as_of_all_enterprises",
    "total_innovation_expenditure_in_1_000_euro",
    "innovation_expenditure_in_1_000_euro_in_house_r_d",
    "innovation_expenditure_in_1_000_euro_external_r_d",
    "innovation_expenditure_in_1_000_euro_acquisition_of_machinery_equipment_software_buildings",
    "innovation_expenditure_in_1_000_euro_acquisition_of_external_knowledge",
    "innovation_expenditure_in_1_000_euro_other_innovation_expenditure"
FROM "statistics-austria-ogd-innov005-cis-005-unt-innovation-1"
