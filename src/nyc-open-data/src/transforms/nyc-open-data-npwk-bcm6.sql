-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "report_type",
    "borough",
    "region",
    "district",
    "school",
    "school_name",
    "_program" AS program,
    "grade_or_service_category",
    "core_course_high_schools_only",
    "average_class_size",
    "pupil_teacher_ratio_ptr_all_students",
    "ptr_excluding_special_ed"
FROM "nyc-open-data-npwk-bcm6"
