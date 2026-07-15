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
    "intake"
FROM "sg-data-d-e67121030a86654f2a77ee7c5fd5a985"
