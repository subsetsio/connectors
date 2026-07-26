-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "at_fcrc_in_fy_2015_yesno",
    "fy_2015_registration_yesno",
    "registration_date_or_date_sent_to_comptroller_for_registration",
    "value_for_fy2015_registrations",
    "doc_cd_eg_rct1",
    "doc_agency_code",
    "doc_id_automatically_generated_contract_id_number_from_fms",
    "concession_id_preregistration",
    "concessionaire",
    "concession_type_specific_category",
    "concession_type_general_category",
    "solicitationaward_method",
    "start_date",
    "expiration_date",
    "revenue_collected_in_fy_2015",
    "brief_description_of_concession",
    "borough"
FROM "nyc-open-data-7kc8-z939"
