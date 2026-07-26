-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "fy_2015_award_or_transaction_yesno",
    "fy_2015_registration_yesno",
    "franchisee",
    "registration_date_or_date_sent_to_comptroller_for_registration",
    "registration_value_for_fy_2015_transactions",
    "doc_cd_eg_rct1",
    "doc_agency_code",
    "doc_id_automatically_generated_contract_id_number_from_fms",
    "franchise_type_specific_category",
    "franchise_type_general_category",
    "solicitationaward_method",
    "start_date",
    "expiration_date",
    "actual_feerevenue_collected_in_fy2015",
    "public_hearing_date_if_applicable",
    "public_meeting_date_if_applicable",
    "brief_description_of_franchise_award_or_fy2015_transaction"
FROM "nyc-open-data-rbvx-jqnh"
