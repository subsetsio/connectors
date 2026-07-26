-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_visited",
    "agency",
    "site_id",
    "service_center",
    "site_address",
    "borough",
    "secret_shopper_language",
    "interaction_with_security_guards",
    "interaction_with_reception_staff",
    "interaction_with_frontline_staff",
    "does_facility_have_signs_posted_notifying_clients_to_the_right_of_interpretation_services",
    "languages_in_which_the_facility_has_translated_signs_relating_to_service_being_provided",
    "languages_in_which_the_facility_has_translated_documents",
    "method_in_which_interpretation_was_made_available",
    "time_spent_waiting_for_an_interpreter_after_speaking_to_staff_member",
    "did_the_secret_shopper_receive_the_information_or_service_asked_for",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-3m3d-zzwn"
