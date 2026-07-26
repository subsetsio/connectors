-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "sy20202021_total_students_with_initial_referrals_712020_06302021",
    "closed_without_iep_meeting",
    "student_determined_ineligible_iep_meeting_60_calendar_days_from_date_of_consent",
    "student_determined_ineligible_iep_meeting_60_calendar_days_from_date_of_consent_1",
    "total_ineligible",
    "student_classified_iep_meeting_60_calendar_days_from_date_of_consent",
    "student_classified_iep_meeting_60_calendar_days_from_date_of_consent_1",
    "total_classified",
    "total_iep_meetings_held_ineligible_classified",
    "open_and_awaiting_parental_consent_as_of_06302021",
    "open_and_parental_consent_received_as_of_06302021"
FROM "nyc-open-data-epjz-e3up"
