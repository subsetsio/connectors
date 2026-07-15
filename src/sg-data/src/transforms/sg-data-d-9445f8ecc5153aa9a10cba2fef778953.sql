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
    "count"
FROM "sg-data-d-9445f8ecc5153aa9a10cba2fef778953"
