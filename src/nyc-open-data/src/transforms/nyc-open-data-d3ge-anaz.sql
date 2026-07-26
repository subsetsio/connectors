-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "boro",
    "csd",
    "school_code",
    "school_name",
    "grade",
    "program_type",
    "core_subject_ms_core_and_912_only",
    "core_course_ms_core_and_912_only",
    "service_categoryk9_only",
    "number_of_classes",
    "total_register",
    "average_class_size",
    "size_of_smallest_class",
    "size_of_largest_class",
    "data_source",
    "schoolwide_pupilteacher_ratio"
FROM "nyc-open-data-d3ge-anaz"
