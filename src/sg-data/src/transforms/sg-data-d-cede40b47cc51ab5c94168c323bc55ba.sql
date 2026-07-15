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
FROM "sg-data-d-cede40b47cc51ab5c94168c323bc55ba"
