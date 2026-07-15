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
FROM "sg-data-d-120ad7e0334d2c2a37ad62ae262f75fa"
