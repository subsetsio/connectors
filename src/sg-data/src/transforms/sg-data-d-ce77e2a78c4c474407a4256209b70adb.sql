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
    "no_of_students"
FROM "sg-data-d-ce77e2a78c4c474407a4256209b70adb"
