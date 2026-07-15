-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "school",
    "course_name",
    "course_abbreviation",
    "course_code",
    "reference"
FROM "sg-data-d-410aa9ff5ce5617a0cbebe9092c4a2e0"
