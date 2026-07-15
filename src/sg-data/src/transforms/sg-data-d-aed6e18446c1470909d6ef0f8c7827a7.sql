-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "school",
    "course_name",
    "moe_course_code",
    "poly_course_code",
    "course_description",
    "reference"
FROM "sg-data-d-aed6e18446c1470909d6ef0f8c7827a7"
