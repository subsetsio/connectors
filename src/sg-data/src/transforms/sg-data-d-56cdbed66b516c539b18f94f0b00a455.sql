-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "school",
    "course_type",
    "course_name",
    "gender",
    "enrolment"
FROM "sg-data-d-56cdbed66b516c539b18f94f0b00a455"
