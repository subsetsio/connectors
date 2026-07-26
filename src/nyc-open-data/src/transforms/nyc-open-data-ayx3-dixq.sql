-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "record_category",
    "industry",
    "application_submission_date",
    "applicant_name",
    "does_the_organization_currently_hold_an_active_pedicab_business_license",
    "license_number",
    "total_number_of_registered_pedicab_vehicles",
    "desired_number_of_pedicab_units",
    "pedicab_lottery_application_order_number",
    "pedicab_lottery_priority_number",
    "lottery_selection_date",
    "selected_from_lottery",
    "city",
    "state",
    "zip_code",
    "borough",
    "community_district",
    "council_district"
FROM "nyc-open-data-ayx3-dixq"
