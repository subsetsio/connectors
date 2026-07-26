-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "record_type_category",
    "record_type_sub_type",
    "applicant_name",
    "application_submission_date",
    "lottery_application_order_number",
    "lottery_application_order_number_district",
    "lottery_priority_number",
    "lottery_selection_date",
    "selected_from_lottery",
    "license_application_number",
    "city",
    "state",
    "zip_code",
    "borough",
    "community_district"
FROM "nyc-open-data-u42f-se8e"
