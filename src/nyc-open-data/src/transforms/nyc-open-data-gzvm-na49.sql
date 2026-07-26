-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of_date",
    "change_order_project_sca_contract_identifier",
    "change_order_boro_identifier",
    "change_order_project_district_identifier",
    "change_order_project_identifier",
    "change_management_number",
    "change_order_document_date",
    "change_order_project_ball_in_court_code",
    "change_order_project_title",
    "change_order_document_type",
    "change_order_project_stage_date",
    "change_order_number",
    "change_order_project_to_status_name",
    "change_order_project_to_vendor"
FROM "nyc-open-data-gzvm-na49"
