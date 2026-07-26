-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "borough",
    "applied_for_the_program",
    "were_accepted_and_enrolled",
    "average_wage_of_such_residents",
    "received_a_referral_for_social_services_through_the_program",
    "enrolled_in_financial_counseling_services_through_the_program",
    "enrolled_in_collegereadiness_courses_or_participated_in_collegereadiness_activities_through_the_program"
FROM "nyc-open-data-x4x8-m3ds"
