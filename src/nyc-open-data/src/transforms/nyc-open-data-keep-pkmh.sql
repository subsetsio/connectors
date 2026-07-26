-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "as_of_date",
    "complaint_id",
    "tax_id",
    "ccrb_substantiated_officer_disposition",
    "board_discipline_recommendation",
    "nonapu_nypd_penalty_report_date",
    "officer_is_apu",
    "apu_ccrb_trial_recommended_penalty",
    "apu_trial_commissioner_recommended_penalty",
    "apu_plea_agreed_penalty",
    "apu_case_status",
    "apu_closing_date",
    "nypd_officer_penalty"
FROM "nyc-open-data-keep-pkmh"
