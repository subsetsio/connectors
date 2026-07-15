-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Course_Name" AS course_name,
    "Course_Description" AS course_description,
    "Reference" AS reference
FROM "sg-data-d-f6b3f930a5faa82bb1fbeb1d747a8b5b"
