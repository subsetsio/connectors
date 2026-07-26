-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "report_type",
    "borough",
    "csd",
    "school_code",
    "school_name",
    "grade_level",
    "program_type",
    "core_subject_ms_core_and_912_only",
    "core_course_ms_core_and_912_only",
    "service_categoryk9_only",
    "number_of_students_seats_filled",
    "number_of_sections",
    "average_class_size",
    "size_of_smallest_class",
    "size_of_largest_class",
    "data_source",
    "schoolwide_pupilteacher_ratio"
FROM "nyc-open-data-nbpb-zygj"
