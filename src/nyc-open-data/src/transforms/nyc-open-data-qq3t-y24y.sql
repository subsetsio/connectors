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
    "number_of_students_in_grades_68",
    "number_of_students_in_grades_68_who_met_the_health_education_requirements",
    "percentage_of_students_in_grades_68_who_met_the_health_education_requirements",
    "number_of_students_in_grades_68_who_completed_or_were_scheduled_to_complete_at_least_one_semester_of_health_instruction",
    "percentage_of_students_in_grades_68_who_completed_or_were_scheduled_to_complete_at_least_one_semester_of_health_instruction",
    "number_of_of_students_in_grades_68_who_met_or_were_scheduled_to_meet_the_requirement_of_54_hours_of_health_instruction",
    "percentage_of_students_in_grades_68_who_met_or_were_scheduled_to_meet_the_requirement_of_54_hours_of_health_instruction",
    "of_8th_graders",
    "number_of_8th_graders_who_met_the_health_education_requirements",
    "percentage_of_8th_graders_who_met_the_health_education_requirements",
    "number_of_8th_graders_who_completed_or_were_scheduled_to_complete_at_least_one_semester_of_health_instruction",
    "percentage_of_8th_graders_who_completed_or_were_scheduled_to_complete_at_least_one_semester_of_health_instruction",
    "numberof_8th_graders_who_met_or_were_scheduled_to_meet_the_requirement_of_54_hours_of_health_instruction",
    "percentage_of_8th_graders_who_met_or_were_scheduled_to_meet_the_requirement_of_54_hours_of_health_instruction"
FROM "nyc-open-data-qq3t-y24y"
