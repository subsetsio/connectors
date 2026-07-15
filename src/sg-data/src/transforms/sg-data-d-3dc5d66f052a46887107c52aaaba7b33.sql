-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "semester",
    "school",
    "jae_course_code",
    "course_name",
    "gender",
    "enrolment"
FROM "sg-data-d-3dc5d66f052a46887107c52aaaba7b33"
