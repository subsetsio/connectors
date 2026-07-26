-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "report_type",
    "school_dbn",
    "school_name",
    "community_school_district",
    "city_council_district",
    "number_of_students_in_grades_912",
    "number_of_students_in_grades_912_who_have_completed_at_least_one_semester_of_health_instruction",
    "percentage_of_students_in_grades_912_who_have_completed_at_least_one_semester_of_health_instruction",
    "number_of_students_in_grades_912_who_have_scheduled_at_least_one_semester_of_health_instruction",
    "percentage_of_students_in_grades_912_who_have_scheduled_at_least_one_semester_of_health_instruction",
    "number_of_june_and_august_graduates",
    "number_of_june_and_august_graduates_meeting_high_school_health_requirements",
    "percentage_of_june_and_august_graduates_meeting_high_school_health_requirements"
FROM "nyc-open-data-msnn-ey3g"
