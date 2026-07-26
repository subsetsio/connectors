-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_year",
    "agency_name",
    "total_number_of_foil_responses_that_included_the_release_of_any_data_public_dataset_or_not",
    "number_of_foil_responses_that_included_the_release_of_a_public_dataset_neither_published_nor_scheduled_for_release_on_nyc_open_data",
    "number_of_foil_responses_that_included_the_sharing_of_a_public_dataset_already_published_or_scheduled_for_release_on_nyc_open_data",
    "number_of_foil_responses_that_resulted_in_data_being_posted_voluntarily_on_nyc_open_data",
    "total_number_of_foil_responses_that_includes_a_public_data_set_not_yet_published_on_the_open_data_portal",
    "notes"
FROM "nyc-open-data-w462-digi"
