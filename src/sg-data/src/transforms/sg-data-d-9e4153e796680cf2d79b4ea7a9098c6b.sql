-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "school",
    "course_name",
    "course_description",
    "reference"
FROM "sg-data-d-9e4153e796680cf2d79b4ea7a9098c6b"
