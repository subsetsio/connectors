-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "school",
    "course_name",
    "course_code",
    "course_description",
    "reference"
FROM "sg-data-d-351bb7940ca11e8fa28a6dfc56e2f2c9"
