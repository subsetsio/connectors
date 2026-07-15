-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "jae_course_code",
    "course_name",
    "url"
FROM "sg-data-d-93384114c34e72d1cb7908b95618267a"
