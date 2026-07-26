-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "nycha_development",
    "borough",
    "total_number_of_resident_job_placements",
    "average_wage_of_such_residents",
    "total_number_of_resident_connections_to_services",
    "total_number_of_residents_that_applied_for_the_nycha_resident_training_academy",
    "total_number_of_residents_that_were_accepted_and_enrolled",
    "total_number_residents_placed_into_fulltime_or_parttime_jobs",
    "average_wage_of_such_residents_1",
    "number_of_residents_that_enrolled_in_financial_counseling_servicesworkshops_through_the_rees_zone_partner_program",
    "total_number_of_residents_enrolled_in_vocational_training_programs_through_the_program",
    "total_number_of_residents_enrolled_in_prep_courses_for_english_as_a_second_language_esol_or_the_test_assessing_secondary_completion_tasc_through_the_program"
FROM "nyc-open-data-dggd-3jfu"
