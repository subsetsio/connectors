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
    "enteprises_with_product_innovations",
    "enteprises_with_product_innovations_as_of_all_enterprises",
    "enteprises_with_process_innovations",
    "enteprises_with_process_innovations_as_of_all_enterprises",
    "enterprises_with_innovation_activities_abandoned_before_completion",
    "enterprises_with_innovation_activities_abandoned_before_completion_as_of_all_enterprises",
    "enterprises_with_innovation_activities_still_ongoing_at_the_end_of_the_reference_year",
    "enterprises_with_innovation_activities_still_ongoing_at_the_end_of_the_reference_year_as_of_all_enterprises",
    "enteprises_with_non_technological_innovations",
    "enteprises_with_non_technological_innovations_as_of_all_enterprises",
    "enterprises_with_organisational_innovations",
    "enterprises_with_organisational_innovations_as_of_all_enterprises",
    "enterprises_with_marketing_innovations",
    "enterprises_with_marketing_innovations_as_of_all_enterprises"
FROM "statistics-austria-ogd-innov001-cis-001-unt-innovation-1"
