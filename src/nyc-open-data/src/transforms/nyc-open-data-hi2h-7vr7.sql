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
    "grade_level",
    "number_of_students",
    "number_of_students_that_received_the_required_number_of_lessons_in_hivaids_education",
    "percentage_of_students_that_received_the_required_number_of_lessons_in_hivaids_education",
    "number_of_students_in_grade_6",
    "number_of_students_in_grade_6_received_5_lessons_in_hivaids_education",
    "percentage_of_students_in_grade_6_received_5_lessons_in_hivaids_education",
    "number_of_students_in_grades_712",
    "number_of_students_in_grades_712_received_6_lessons_in_hivaids_education",
    "percentage_of_students_in_grades_712_received_6_lessons_in_hivaids_education"
FROM "nyc-open-data-hi2h-7vr7"
