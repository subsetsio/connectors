-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "caseid",
    "students_community_school_district_of_residence",
    "students_representative_attorney_nonattorney_advocate_nonepro_se",
    "date_on_which_doe_received_the_due_process_complaint_or_tenday_notice",
    "date_on_which_doe_referred_for_settlement",
    "date_on_which_the_parent_and_doe_agreed_to_a_proposed_written_settlement_agreement_that_may_be_subject_to_additional_required_approvals",
    "date_on_which_doe_received_all_necessary_approvals_and_authority_necessary_to_sign_a_written_settlement_agreement",
    "date_doe_received_signed_proposed_written_settlement_agreement_from_parent",
    "date_doe_approved_written_settlement_agreement_for_payment",
    "date_doe_issued_first_payment_pursuant_to_written_settlement_agreement"
FROM "nyc-open-data-ekck-c5sb"
