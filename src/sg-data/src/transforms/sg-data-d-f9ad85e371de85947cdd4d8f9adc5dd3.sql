-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course-code" AS course_code,
    "course-title" AS course_title
FROM "sg-data-d-f9ad85e371de85947cdd4d8f9adc5dd3"
