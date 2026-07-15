-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "School" AS school,
    "Course_Name" AS course_name,
    "Course_Code" AS course_code,
    "Course_Description" AS course_description,
    "Reference" AS reference
FROM "sg-data-d-913f2d358c89139a12b7c1c7133caa04"
