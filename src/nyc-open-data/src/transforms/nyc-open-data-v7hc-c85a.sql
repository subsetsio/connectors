-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "borough",
    "applied_for_the_program",
    "were_accepted_and_enrolled",
    "were_placed_into_fulltime_or_parttime_jobs",
    "average_wage",
    "received_a_referral_for_social_services_through_the_program",
    "enrolled_in_financial_counseling_services_through_the_program",
    "enrolled_in_vocational_training_programs_through_the_program",
    "enrolled_in_prep_courses_for_english_as_a_second_language_esol_or_the_test_assessing_secondary_completion_tasc_through_the_program",
    "enrolled_in_collegereadiness_courses_or_participated_in_collegereadiness_activities_through_the_program"
FROM "nyc-open-data-v7hc-c85a"
