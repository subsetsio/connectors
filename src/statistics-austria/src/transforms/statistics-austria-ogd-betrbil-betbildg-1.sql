-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_series" AS BIGINT) AS time_series,
    "economic_activities_and_size_classes",
    "enterprises_with_continuing_vocational_training_in",
    "enterprises_with_cvt_courses_in",
    "enterprises_with_other_forms_of_cvt_in",
    "enterprises_with_guided_on_the_job_training_in",
    "enterprises_with_job_rotation_in",
    "enterprises_with_learning_or_quality_circles_in",
    "enterprises_with_self_directed_learning_in",
    "enterprises_with_training_at_trade_fairs_conferences_etc_in",
    "cvt_course_participation_in",
    "cvt_course_participation_of_men_in",
    "cvt_course_participation_of_women_in",
    "share_of_internal_training_course_hours_in",
    "share_of_external_training_course_hours_in",
    "cvt_course_hours_per_person_employed",
    "cvt_course_hours_per_participant",
    "total_costs_of_cvt_courses_as_of_personnel_costs",
    "total_costs_of_cvt_courses_per_person_employed_in",
    "total_costs_of_cvt_courses_per_participant_in",
    "total_costs_of_cvt_courses_per_course_hour_in",
    "direct_costs_of_cvt_courses_per_person_employed_in",
    "direct_costs_of_cvt_courses_per_participant_in",
    "direct_costs_of_cvt_courses_per_course_hour_in"
FROM "statistics-austria-ogd-betrbil-betbildg-1"
