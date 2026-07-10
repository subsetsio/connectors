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
    "enteprises_with_innovation_activities",
    "enteprises_with_innovation_activities_as_of_all_enterprises",
    "enteprises_with_technological_innovations",
    "enteprises_with_technological_innovations_as_of_all_enterprises",
    "enteprises_with_other_product_innovations",
    "enteprises_with_other_product_innovations_as_of_all_enterprises",
    "enterprises_with_innovation_activities_abandoned_before_completion",
    "enterprises_with_innovation_activities_abandoned_before_completion_as_of_all_enterprises",
    "enterprises_with_innovation_activities_not_completed_before_the_end_of_2018",
    "enterprises_with_innovation_activities_not_completed_before_the_end_of_2018_as_of_all_enterprises",
    "enterprises_with_r_d_activities",
    "enterprises_with_r_d_activities_as_of_all_enterprises"
FROM "statistics-austria-ogd-innov011-cis-011-unt-innovation-1"
