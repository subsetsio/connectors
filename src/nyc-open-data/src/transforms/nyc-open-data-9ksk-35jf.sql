-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "report_type",
    "borough",
    "csd",
    "grade_level",
    "program_type",
    "core_subject",
    "service_category",
    "class_size",
    "number_of_classes",
    "number_of_students",
    "percent_of_students_in_borough_grade_program_subject"
FROM "nyc-open-data-9ksk-35jf"
