-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "overall_attendance_rate",
    "remote_students_online_attendance_rate",
    "blended_students_overall_attendance_rate",
    "blended_students_inperson_attendance_rate",
    "blended_students_online_attendance_rate"
FROM "nyc-open-data-5e7z-xsdf"
